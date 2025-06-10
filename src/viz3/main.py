import argparse
import subprocess
import sys
import os
import time

from viz3.config_parser import parse_args


def start_window(args, window_index: int = 0):
    """Start a window process.

    Args:
        args: Parsed command line arguments
        window_index: Index of the window for positioning

    Returns:
        subprocess.Popen: The started process
    """
    cmd = (
        [sys.executable, "-m", "viz3.viz3"]
        + sys.argv[1:]
        + [f"--window_index={window_index}"]
    )
    process = subprocess.Popen(cmd)
    return process


def main() -> None:
    """Main entry point for the application."""
    args = parse_args()
    processes = []
    for i in range(args.number_of_windows_to_open):
        process = start_window(args, i)
        processes.append(process)
        print(f"Started window process {i+1} with PID: {process.pid}")

    try:
        while any(process.poll() is None for process in processes):
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("\nReceived interrupt signal. Shutting down processes...")
        for process in processes:
            process.terminate()
        for process in processes:
            process.wait()
        print("All processes terminated.")


if __name__ == "__main__":
    main()
