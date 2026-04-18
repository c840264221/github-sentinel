# core/scheduler.py

import time


def start_scheduler(job_func, interval_seconds=60):
    print("⏰ Scheduler started...")

    while True:
        print("🔄 Running scheduled job...")

        try:
            job_func()
        except Exception as e:
            print(f"❌ Error: {e}")

        print(f"😴 Sleeping for {interval_seconds} seconds...\n")
        time.sleep(interval_seconds)