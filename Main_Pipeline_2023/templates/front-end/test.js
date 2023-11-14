// Read the input text file
import * as fs from "fs";

const resultArray = [];

fs.readFile('unique.txt', 'utf8', (err, data) => {
    if (err) {
        console.error('Error reading the file:', err);
        return;
    }

    // Split the file content into lines
    const lines = data.trim().split('\n');

    // Initialize an empty array to store the result

    // Process each line to create the desired object and add it to the result array
    lines.forEach((line, index) => {
        const label = line.trim();
        const value = label;
        resultArray.push({ label, value });
        // Add the corresponding Arabic entry
    });

    console.log(resultArray);
    const outputFilename = 'output.js';

    const jsCode = `const myOptions = ${JSON.stringify(resultArray, null, 2)};\n\nexport default outputArray;\n`;

    fs.writeFile(outputFilename, jsCode, (err) => {
        if (err) {
            console.error('Error writing to the file:', err);
        } else {
            console.log(`Result array saved to ${outputFilename}`);
        }
    });
});


