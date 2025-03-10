import asyncio
import json
import sys
from pathlib import Path
from datetime import datetime

# Add the project root to Python path
sys.path.append(str(Path(__file__).parent))

from src.main import run_job_search

async def main():
    # Read the test resume
    with open('test_resume.txt', 'r') as f:
        resume_text = f.read()
    
    print("Starting job search...")
    print("Resume loaded, length:", len(resume_text))
    
    try:
        # Run the job search
        result = await run_job_search(resume_text)
        
        # Save results to a file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f'job_search_results_{timestamp}.json'
        
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        
        print(f"\nJob search completed successfully!")
        print(f"Results saved to: {output_file}")
        
        # Print summary
        if "job_listings" in result:
            print(f"\nFound {len(result['job_listings'])} matching jobs:")
            for idx, job in enumerate(result['job_listings'], 1):
                print(f"\n{idx}. {job.get('title', 'No title')} at {job.get('company', 'No company')}")
                print(f"   Location: {job.get('location', 'No location')}")
                print(f"   Score: {job.get('initial_score', 'No score')}")
    
    except Exception as e:
        print(f"Error during job search: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 