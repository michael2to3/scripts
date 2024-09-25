# Keycloak Password Spraying Tool

This is a Node.js-based tool using Puppeteer for performing password spraying attacks on Keycloak authentication portals. It automates login attempts by cycling through a list of usernames and passwords, with support for additional features like cookie resets and handling login failures.

## Features

- Automates password spraying attacks on Keycloak.
- Cycles through usernames and passwords with configurable delays.
- Supports debug mode with visible browser actions.
- Resets cookies after successful login with `--continue` option.
- Detects login failures based on page content.

## Prerequisites

- Node.js v14+ installed
- Puppeteer package installed (automatically with `npm install`)

## Installation

1. Install dependencies:

   ```bash
   npm install
   ```

## Usage

Run the script with the required arguments:

```bash
node main.js --target=<url> --logins=<path_to_logins_file> --passwords=<path_to_passwords_file> [--output=<output_file>] [--delay=<delay_in_ms>] [--debug] [--continue]
```

### Example

```bash
node main.js --target='https://example-keycloak.com/' --logins=logins.txt --passwords=passwords.txt --output=results.log --delay=5000 --debug --continue
```

### Options

- `--target`: URL of the Keycloak login page (required).
- `--logins`: Path to the file containing usernames (required).
- `--passwords`: Path to the file containing passwords (required).
- `--output`: Output file for logging results (default: `output.log`).
- `--delay`: Delay between login attempts in milliseconds (default: `1000`).
- `--debug`: Enable debug mode with additional logs and a visible browser.
- `--continue`: Continue login attempts after successful login (resets cookies).
