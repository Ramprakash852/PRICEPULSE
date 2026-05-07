from apscheduler.schedulers.blocking import BlockingScheduler
import os

scheduler = BlockingScheduler()

@scheduler.scheduled_job("interval", hours=6)
def automated_pipeline():

    print("Running scraping pipeline...")

    os.system("python app/scraper/scraper.py")
    os.system("python app/cleaning/clean_data.py")
    os.system("python -m app.database.insert_data")

    print("Pipeline completed!")

scheduler.start()