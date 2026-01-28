#!/usr/bin/env python3
"""Run tests for a specific feature or all features.

Usage:
    python scripts/run_feature_tests.py          # Run all tests
    python scripts/run_feature_tests.py 001      # Run tests for feature 001
    python scripts/run_feature_tests.py 002      # Run tests for feature 002
    python scripts/run_feature_tests.py --cov    # Run all tests with coverage
"""

import subprocess
import sys
from pathlib import Path


def main():
    args = sys.argv[1:]

    # Base pytest command
    cmd = ["python", "-m", "pytest"]

    # Check for coverage flag
    if "--cov" in args:
        cmd.extend(["--cov=src/stockagent", "--cov-report=term-missing"])
        args.remove("--cov")

    # Check for feature number
    if args and args[0].isdigit():
        feature_num = args[0].zfill(3)
        # Run tests marked with the feature marker
        cmd.extend(["-m", f"feature{feature_num}", "-v"])
        print(f"Running tests for feature {feature_num}...")
    else:
        cmd.append("-v")
        print("Running all tests...")

    # Change to project root
    project_root = Path(__file__).parent.parent

    # Run pytest
    result = subprocess.run(cmd, cwd=project_root)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
