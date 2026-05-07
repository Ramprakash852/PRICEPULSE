"""
Pipeline Run History Viewer
Displays the history of automated pipeline executions
"""

import json
import os
from datetime import datetime
from tabulate import tabulate

RUNS_LOG = "logs/pipeline_runs.json"

def view_pipeline_runs(limit=20):
    """Display pipeline run history"""
    
    if not os.path.exists(RUNS_LOG):
        print("❌ No pipeline runs history found.")
        print(f"   Path: {RUNS_LOG}")
        return
    
    try:
        with open(RUNS_LOG, 'r') as f:
            runs = json.load(f)
    except Exception as e:
        print(f"❌ Error reading runs log: {e}")
        return
    
    if not runs:
        print("❌ No pipeline runs recorded yet.")
        return
    
    # Get last N runs
    recent_runs = runs[-limit:]
    recent_runs.reverse()  # Show newest first
    
    print("\n" + "=" * 100)
    print("📊 PIPELINE RUN HISTORY")
    print("=" * 100)
    
    # Prepare table data
    table_data = []
    for i, run in enumerate(recent_runs, 1):
        timestamp = run.get("timestamp", "N/A")
        status = run.get("status", "unknown")
        
        # Parse details
        details = run.get("details", {})
        scraper = details.get("scraper", "N/A")
        cleaner = details.get("cleaner", "N/A")
        inserter = details.get("inserter", "N/A")
        
        # Status emoji
        status_emoji = "✅" if status == "success" else "❌"
        
        # Convert timestamp to readable format
        try:
            dt = datetime.fromisoformat(timestamp)
            readable_time = dt.strftime("%Y-%m-%d %H:%M:%S")
        except:
            readable_time = timestamp
        
        table_data.append([
            i,
            readable_time,
            status_emoji,
            scraper,
            cleaner,
            inserter
        ])
    
    headers = ["#", "Timestamp", "Status", "Scraper", "Cleaner", "Inserter"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    print("=" * 100)
    
    # Summary statistics
    total_runs = len(runs)
    successful_runs = sum(1 for r in runs if r.get("status") == "success")
    failed_runs = total_runs - successful_runs
    success_rate = (successful_runs / total_runs * 100) if total_runs > 0 else 0
    
    print(f"\n📈 Summary (Last {limit} runs):")
    print(f"   Total runs: {len(recent_runs)}")
    print(f"   Successful: {sum(1 for r in recent_runs if r.get('status') == 'success')}")
    print(f"   Failed: {sum(1 for r in recent_runs if r.get('status') == 'failed')}")
    
    print(f"\n📊 All-time Statistics (All {total_runs} runs):")
    print(f"   Total runs: {total_runs}")
    print(f"   Successful: {successful_runs}")
    print(f"   Failed: {failed_runs}")
    print(f"   Success rate: {success_rate:.1f}%")
    print()

if __name__ == "__main__":
    view_pipeline_runs()
