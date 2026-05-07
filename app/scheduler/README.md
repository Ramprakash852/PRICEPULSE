# Scheduler Documentation

The PricePulse scheduler automates the data pipeline to run at regular intervals.

## Features

- **Automated Pipeline Execution**: Runs scraper → cleaner → database insert every 6 hours
- **Comprehensive Logging**: All pipeline activity logged to `logs/pipeline.log`
- **Run History Tracking**: Each execution recorded in `logs/pipeline_runs.json`
- **Success/Failure Tracking**: Detailed status for each pipeline component
- **Run History Viewer**: Command-line utility to view execution history

## Running the Scheduler

### Start the Scheduler

```bash
python app/scheduler/scheduler.py
```

The scheduler will run indefinitely, executing the pipeline every 6 hours. Press `Ctrl+C` to stop.

### View Pipeline Run History

```bash
python app/scheduler/view_runs.py
```

This displays:
- Recent execution timestamps
- Status of each pipeline component (Scraper, Cleaner, Inserter)
- Summary statistics (success rate, total runs, etc.)

## Log Files

Logs are stored in the `logs/` directory:

### `logs/pipeline.log`
Detailed execution log with timestamps:
```
2026-05-07 14:32:15,123 - INFO - 🚀 STARTING AUTOMATED PIPELINE
2026-05-07 14:32:16,456 - INFO - 📥 Step 1: Running Web Scraper...
2026-05-07 14:32:45,789 - INFO - ✅ Scraper completed successfully in 29.33s
...
```

### `logs/pipeline_runs.json`
Structured history of all runs (last 100 kept):
```json
[
  {
    "timestamp": "2026-05-07T14:32:15.123456",
    "status": "success",
    "details": {
      "scraper": "success",
      "cleaner": "success",
      "inserter": "success",
      "overall": "success",
      "error_messages": []
    }
  }
]
```

## Pipeline Components

1. **Scraper** (`app/scraper/scraper.py`)
   - Fetches product data using Playwright
   - Saves to `app/scraper/raw_data.csv`

2. **Cleaner** (`app/cleaning/clean_data.py`)
   - Removes duplicates and normalizes data
   - Saves to `app/cleaning/cleaned_data.csv` and `cleaned_data.json`

3. **Inserter** (`app/database/insert_data.py`)
   - Loads cleaned data into PostgreSQL
   - Records price snapshots in history table

## Monitoring

### Real-time Monitoring

Watch the logs in real-time:

```bash
# Windows
Get-Content -Path logs/pipeline.log -Wait

# Mac/Linux
tail -f logs/pipeline.log
```

### View Recent Runs

```bash
python app/scheduler/view_runs.py
```

Sample output:
```
====================================================
📊 PIPELINE RUN HISTORY
====================================================
#  Timestamp                     Status  Scraper  Cleaner  Inserter
1  2026-05-07 14:32:15           ✅      success  success  success
2  2026-05-07 08:45:22           ✅      success  success  success
3  2026-05-07 02:15:10           ❌      failed   N/A      N/A

📊 Summary (Last 20 runs):
   Successful: 18
   Failed: 2
   Success rate: 90.0%
```

## Troubleshooting

### No Logs Directory

The scheduler automatically creates the `logs/` directory on first run.

### Pipeline Failed

Check `logs/pipeline.log` for detailed error messages. Each component logs:
- Start time
- Duration
- Success/failure status
- Error details (if failed)

### Database Connection Issues

Ensure:
1. PostgreSQL is running
2. `.env` has correct `DATABASE_URL`
3. Database exists and is accessible

### File Not Found Errors

Verify the scheduler runs from the project root:
```bash
cd c:\Users\chitt\Desktop\pricepulse
python app/scheduler/scheduler.py
```

## Future Enhancements

- Email alerts on pipeline failure
- Dashboard widget showing run history
- Configurable schedule intervals
- Retry logic for failed components
- Slack/Discord notifications
