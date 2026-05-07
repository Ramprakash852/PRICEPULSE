"""
Quick Database Fix
Run this script to repair database schema mismatch
"""

import subprocess
import sys
import os

def main():
    print("=" * 80)
    print("🔧 PricePulse Database Quick Fix")
    print("=" * 80)
    
    print("\n⚠️  Database schema is out of sync with models")
    print("\nThe products table is missing the 'created_at' column")
    print("The price_history table doesn't exist")
    
    print("\n" + "=" * 80)
    print("SOLUTION OPTIONS")
    print("=" * 80)
    
    print("\nOption 1: Auto-migrate (Recommended)")
    print("  - Adds missing columns")
    print("  - Creates missing tables")
    print("  - Keeps existing data")
    print("  - Safe to run anytime")
    
    print("\nOption 2: Full recreation")
    print("  - Deletes ALL data")
    print("  - Recreates all tables from scratch")
    print("  - Use only if migration fails")
    
    print("\n" + "=" * 80)
    
    choice = input("\nSelect option (1 or 2): ").strip()
    
    # Get the project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    if choice == "1":
        print("\n🔄 Running auto-migration...")
        result = subprocess.run(
            [sys.executable, os.path.join(project_root, "app", "database", "migrate.py")],
            cwd=project_root,
            env={**os.environ, "PYTHONPATH": project_root}
        )
        
        if result.returncode == 0:
            print("\n✅ Migration successful!")
            print("\nYou can now start the API:")
            print("  uvicorn app.api.main:app --reload")
        else:
            print("\n❌ Migration failed")
            sys.exit(1)
    
    elif choice == "2":
        print("\n⚠️  This will DELETE all data!")
        result = subprocess.run(
            [sys.executable, os.path.join(project_root, "app", "database", "migrate.py")],
            cwd=project_root,
            env={**os.environ, "PYTHONPATH": project_root}
        )
        
        if result.returncode == 0:
            print("\n✅ Tables recreated!")
            print("\nNext steps:")
            print("  1. Run scraper: python app/scraper/scraper.py")
            print("  2. Run cleaner: python app/cleaning/clean_data.py")
            print("  3. Insert data: python -m app.database.insert_data")
            print("  4. Start API: uvicorn app.api.main:app --reload")
        else:
            print("\n❌ Recreation failed")
            sys.exit(1)
    
    else:
        print("Invalid option")
        sys.exit(1)

if __name__ == "__main__":
    main()
