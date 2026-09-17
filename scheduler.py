"""Runs run_pipeline.py every INTERVAL_SECONDS (5 minutes by default).

If one run takes longer than the interval, the next run starts right after
it finishes instead of overlapping - increase INTERVAL_SECONDS if that
happens often.

Run from the repository root, and leave it running:
    python scheduler.py
"""
import subprocess
import sys
import time

INTERVAL_SECONDS = 300  # 5 minutes; raise this if a run regularly takes longer

if __name__ == "__main__":
    while True:
        start = time.time()
        subprocess.run([sys.executable, "run_pipeline.py"])
        elapsed = time.time() - start
        sleep_for = max(0, INTERVAL_SECONDS - elapsed)
        print(f"\nrun took {elapsed:.1f}s, sleeping {sleep_for:.1f}s before next run")
        time.sleep(sleep_for)
