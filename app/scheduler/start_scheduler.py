"""
Scheduler Startup Script
Starts the automated pipeline scheduler with enhanced error handling
"""

import subprocess
import sys
import os

def start_scheduler():
    """Start the PricePulse scheduler"""
    
    print("=" * 80)
    print("🚀 PricePulse Scheduler Startup")
    print("=" * 80)
    
    # Check if running from correct directory
    if not os.path.exists("app/scheduler/scheduler.py"):
        print("\n❌ ERROR: scheduler.py not found!")
        print("Please run this script from the project root directory:")
        print("   cd c:\\Users\\chitt\\Desktop\\pricepulse")
        print("   python app/scheduler/start_scheduler.py")
        sys.exit(1)
    
    # Check if venv is activated
    if sys.prefix == sys.base_prefix:
        print("\n⚠️  WARNING: Virtual environment not activated!")
        print("Activate venv first:")
        print("   venv\\Scripts\\activate")
        response = input("\nContinue anyway? (y/n): ").lower()
        if response != 'y':
            sys.exit(0)
    
    print("\n✅ Checks passed!")
    print("📁 Project root: " + os.getcwd())
    print("📊 Logs directory: " + os.path.abspath("logs"))
    
    print("\n" + "=" * 80)
    print("Starting scheduler...")
    print("Pipeline will run every 6 hours")
    print("Press Ctrl+C to stop")
    print("=" * 80 + "\n")
    
    try:
        # Start the scheduler
        subprocess.run([sys.executable, "app/scheduler/scheduler.py"], 
                      check=True,
                      cwd=os.getcwd())
    
    except KeyboardInterrupt:
        print("\n\n" + "=" * 80)
        print("⏹️  Scheduler stopped by user")
        print("=" * 80)
        
        # Show option to view runs
        print("\nWould you like to view the run history?")
        response = input("View runs? (y/n): ").lower()
        if response == 'y':
            subprocess.run([sys.executable, "app/scheduler/view_runs.py"],
                          cwd=os.getcwd())
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_scheduler()
