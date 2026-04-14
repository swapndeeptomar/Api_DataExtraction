import time
import os
import logging
from client import GitHubClient
from processor import DataProcessor
from writer import CSVWriter
from logger_config import setup_logging

logger = setup_logging()

CHECKPOINT_FILE = "data/checkpoint.txt"

def get_last_page():
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, "r") as f:
            return int(f.read().strip())
    return 1

def save_checkpoint(page):
    with open(CHECKPOINT_FILE, "w") as f:
        f.write(str(page))

def run_pipeline(search_query: str = "language:python", max_pages: int = 10):
    client = GitHubClient()
    processor = DataProcessor()
    writer = CSVWriter("data/github_repos.csv")
    
    start_page = get_last_page()
    
    if start_page == 1:
        writer.clear_file()
        logger.info("🚀 Starting fresh ETL Pipeline...")
    else:
        logger.info(f"🔄 Resuming ETL Pipeline from page {start_page}...")

    current_page = start_page
    try:
        while current_page <= max_pages:
            logger.info(f"📦 Extracting Page {current_page}...")
            raw_data, links = client.fetch_repositories(query=search_query, page=current_page)
            
            if not raw_data:
                logger.error("🛑 Extraction failed. Check logs.")
                break

            items = raw_data.get('items', [])
            if not items:
                logger.warning("⚠️ No more data found.")
                break
                
            clean_data = processor.flatten_repo_data(items)
            writer.write_batch(clean_data)
            
            logger.info(f"✅ Saved {len(clean_data)} records from page {current_page}.")
            
            # Update state
            current_page += 1
            save_checkpoint(current_page)

            if 'next' not in links:
                logger.info("🏁 No more pages available.")
                os.remove(CHECKPOINT_FILE) # Clean up on full success
                break
                
            time.sleep(2)

    except Exception as e:
        logger.critical(f"💥 Pipeline crashed: {e}", exc_info=True)
    
    logger.info("🏁 Job Finished.")

if __name__ == "__main__":
    run_pipeline()