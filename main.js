// This file is just a placeholder to satisfy Apify's default behavior
// The actual code is in src/main.py and will be run by the Dockerfile

console.log('Redirecting to Python code...');
const { execSync } = require('child_process');
try {
    console.log('Running Python code...');
    const output = execSync('python -m src.main', { stdio: 'inherit' });
    console.log('Python code executed successfully');
} catch (error) {
    console.error('Error running Python code:', error);
    process.exit(1);
} 