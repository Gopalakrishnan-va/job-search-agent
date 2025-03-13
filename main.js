// This is the main entry point for the Apify actor
// It will execute the Python code using child_process

const { execSync } = require('child_process');
const { Actor } = require('apify');

// Initialize the Apify SDK
Actor.main(async () => {
    console.log('Starting Job Search Agent...');
    
    try {
        // Execute the Python script
        console.log('Running Python code...');
        execSync('python -m src.main', { 
            stdio: 'inherit',
            env: {
                ...process.env,
                // Make sure environment variables are passed to the Python process
                APIFY_TOKEN: process.env.APIFY_TOKEN,
                OPENAI_API_KEY: process.env.OPENAI_API_KEY
            }
        });
        
        console.log('Python code executed successfully');
    } catch (error) {
        console.error('Error running Python code:', error);
        throw error;
    }
}); 