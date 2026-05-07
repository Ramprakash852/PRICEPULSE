from apscheduler.schedulers.blocking import BlockingScheduler
from app.utils.logger import logger
import os
import sys
from datetime import datetime
import json

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Configure file logging for scheduler
import logging
file_handler = logging.FileHandler("logs/pipeline.log")
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(file_handler)

# Create a runs log file
RUNS_LOG = "logs/pipeline_runs.json"

def log_run(status, details):
    """Log pipeline run to JSON file for tracking"""
    run_record = {
        "timestamp": datetime.now().isoformat(),
        "status": status,
        "details": details
    }
    
    runs = []
    if os.path.exists(RUNS_LOG):
        try:
            with open(RUNS_LOG, 'r') as f:
                runs = json.load(f)
        except:
            runs = []
    
    runs.append(run_record)
    
    # Keep last 100 runs
    runs = runs[-100:]
    
    with open(RUNS_LOG, 'w') as f:
        json.dump(runs, f, indent=2)

scheduler = BlockingScheduler()

@scheduler.scheduled_job("interval", hours=6)
def automated_pipeline():
    """Automated data pipeline: scrape -> clean -> insert"""
    
    logger.info("=" * 80)
    logger.info("🚀 STARTING AUTOMATED PIPELINE")
    logger.info("=" * 80)
    
    start_time = datetime.now()
    run_status = {
        "scraper": None,
        "cleaner": None,
        "inserter": None,
        "overall": "success",
        "error_messages": []
    }
    
    try:
        # ========== STEP 1: SCRAPING ==========
        logger.info("\n📥 Step 1: Running Web Scraper...")
        scraper_start = datetime.now()
        
        scraper_result = os.system("python app/scraper/scraper.py")
        
        if scraper_result == 0:
            scraper_duration = (datetime.now() - scraper_start).total_seconds()
            logger.info(f"✅ Scraper completed successfully in {scraper_duration:.2f}s")
            run_status["scraper"] = "success"
        else:
            logger.error(f"❌ Scraper failed with exit code {scraper_result}")
            run_status["scraper"] = "failed"
            run_status["overall"] = "failed"
            run_status["error_messages"].append(f"Scraper failed (exit code: {scraper_result})")
        
        # ========== STEP 2: CLEANING ==========
        logger.info("\n🧹 Step 2: Running Data Cleaning Pipeline...")
        cleaner_start = datetime.now()
        
        cleaner_result = os.system("python app/cleaning/clean_data.py")
        
        if cleaner_result == 0:
            cleaner_duration = (datetime.now() - cleaner_start).total_seconds()
            logger.info(f"✅ Cleaner completed successfully in {cleaner_duration:.2f}s")
            run_status["cleaner"] = "success"
        else:
            logger.error(f"❌ Cleaner failed with exit code {cleaner_result}")
            run_status["cleaner"] = "failed"
            run_status["overall"] = "failed"
            run_status["error_messages"].append(f"Cleaner failed (exit code: {cleaner_result})")
        
        # ========== STEP 3: DATABASE INSERT ==========
        logger.info("\n💾 Step 3: Inserting Data into Database...")
        inserter_start = datetime.now()
        
        inserter_result = os.system("python -m app.database.insert_data")
        
        if inserter_result == 0:
            inserter_duration = (datetime.now() - inserter_start).total_seconds()
            logger.info(f"✅ Database insert completed successfully in {inserter_duration:.2f}s")
            run_status["inserter"] = "success"
        else:
            logger.error(f"❌ Database insert failed with exit code {inserter_result}")
            run_status["inserter"] = "failed"
            run_status["overall"] = "failed"
            run_status["error_messages"].append(f"Database insert failed (exit code: {inserter_result})")
        
    except Exception as e:
        logger.error(f"❌ Unexpected error during pipeline execution: {str(e)}")
        run_status["overall"] = "failed"
        run_status["error_messages"].append(f"Unexpected error: {str(e)}")
    
    # ========== FINAL SUMMARY ==========
    total_duration = (datetime.now() - start_time).total_seconds()
    
    logger.info("\n" + "=" * 80)
    logger.info("📊 PIPELINE EXECUTION SUMMARY")
    logger.info("=" * 80)
    logger.info(f"Overall Status: {'✅ SUCCESS' if run_status['overall'] == 'success' else '❌ FAILED'}")
    logger.info(f"Scraper: {run_status['scraper']}")
    logger.info(f"Cleaner: {run_status['cleaner']}")
    logger.info(f"Inserter: {run_status['inserter']}")
    logger.info(f"Total Duration: {total_duration:.2f}s")
    
    if run_status["error_messages"]:
        logger.error("Errors encountered:")
        for error in run_status["error_messages"]:
            logger.error(f"  - {error}")
    
    logger.info("=" * 80 + "\n")
    
    # Log to runs history
    log_run(run_status["overall"], run_status)

# Schedule alternative times for testing (optional)
@scheduler.scheduled_job("cron", hour=0, minute=0)  # Daily at midnight
def daily_pipeline():
    """Daily scheduled pipeline run"""
    logger.info("⏰ Running daily scheduled pipeline...")
    automated_pipeline()

if __name__ == "__main__":
    logger.info("🟢 Scheduler started. Pipeline will run every 6 hours.")
    logger.info(f"Logs directory: {os.path.abspath('logs')}")
    logger.info("Press Ctrl+C to stop the scheduler.\n")
    
    try:
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("⏹️ Scheduler stopped by user")
    except Exception as e:
        logger.error(f"❌ Scheduler encountered an error: {e}")