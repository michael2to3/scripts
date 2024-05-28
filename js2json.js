#!/usr/bin/env node

const {
    stdin,
    stdout
} = require('process');
const acorn = require('acorn');
const safeEval = require('safe-eval');

stdin.setEncoding('utf8');

let data = '';

stdin.on('data', chunk => {
    data += chunk;
});

stdin.on('end', () => {
    try {
        acorn.parse(`(${data})`, {
            ecmaVersion: 2020
        });

        const jsonObject = safeEval(`(${data})`);
        const jsonData = JSON.stringify(jsonObject, null, 4);

        stdout.write(jsonData);
    } catch (error) {
        console.error('Error converting to JSON:', error);
        process.exit(1);
    }
});
