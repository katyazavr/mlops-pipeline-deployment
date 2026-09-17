"""Runs the full pipeline once, end to end:
data engineering -> model engineering -> (re)build and (re)start the API/app
containers with the freshly trained model.

Run from the repository root:
    python run_pipeline.py
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def run(cmd):
    print(f"\n$ {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=ROOT)
    if result.returncode != 0:
        print(f"step failed: {' '.join(cmd)}")
        sys.exit(result.returncode)


def main():
    run([sys.executable, "code/datasets/prepare.py"])
    run([sys.executable, "code/models/train.py"])
    run([
        "docker", "compose",
        "-f", "code/deployment/docker-compose.yml",
        "up", "--build", "-d",
    ])
    print("\npipeline run complete - API on :8000, app on :8501")


if __name__ == "__main__":
    main()
