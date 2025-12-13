const fs = require('fs');
const path = require('path');

// --- Copy of Logic from index.html ---
const parseCSV = (text) => {
    if (!text) return [];
    // Handle possible BOM and normalize line endings
    const cleaned = text.replace(/^\uFEFF/, '');
    const lines = cleaned
        .split(/\r\n|\n/)
        .map((l) => l.trim())
        .filter(Boolean);

    if (lines.length === 0) return [];

    // Robust CSV Line Parser (handles quoted values)
    const parseLine = (line) => {
        const values = [];
        let current = '';
        let inQuote = false;

        for (let i = 0; i < line.length; i++) {
            const char = line[i];
            if (char === '"') {
                inQuote = !inQuote;
            } else if (char === ',' && !inQuote) {
                values.push(current.trim().replace(/^"|"$/g, '').trim());
                current = '';
            } else {
                current += char;
            }
        }

        values.push(current.trim().replace(/^"|"$/g, '').trim());
        return values;
    };

    const headers = parseLine(lines[0]);
    return lines.slice(1).map((line) => {
        const values = parseLine(line);
        const obj = {};
        headers.forEach((h, i) => {
            if (h) obj[h] = values[i] || '';
        });
        return obj;
    });
};

// --- Test Execution ---
const filePath = 'c:/AttritionProject/WA_Fn-UseC_-HR-Employee-Attrition.csv';

try {
    const fileContent = fs.readFileSync(filePath, 'utf8');
    console.log(`Read ${fileContent.length} bytes.`);

    const start = Date.now();
    const parsed = parseCSV(fileContent);
    const end = Date.now();

    console.log(`Parsed ${parsed.length} rows in ${end - start}ms.`);

    if (parsed.length > 0) {
        console.log('Headers detected:', Object.keys(parsed[0]));
        console.log('Sample Row 1:', JSON.stringify(parsed[0], null, 2));
    } else {
        console.error('Parsed 0 rows!');
    }

} catch (err) {
    console.error('Error reading/parsing file:', err);
}
