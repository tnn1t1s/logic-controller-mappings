#!/usr/bin/env python3
"""
Logic Pro Controller Assignment Monitor
--------------------------------------
This script monitors changes to the com.apple.logic.pro.cs file
as you make changes in Logic Pro's Controller Assignments window.

Usage:
  1. Run this script while Logic Pro is running
  2. Make changes in the Controller Assignments window
  3. When you save your changes in Logic, this script will detect and analyze them
"""

import os
import sys
import time
import shutil
import tempfile
import argparse
import subprocess
from pathlib import Path

def get_home_dir():
    """Get the user's home directory."""
    return str(Path.home())

def get_cs_file_path():
    """Get the path to the Logic Pro controller assignment file."""
    home = get_home_dir()
    return os.path.join(home, "Library", "Preferences", "com.apple.logic.pro.cs")

def file_has_changed(file_path, last_modified=None, last_size=None):
    """Check if a file has changed since last check."""
    try:
        stat = os.stat(file_path)
        modified = stat.st_mtime
        size = stat.st_size
        
        if last_modified is None or last_size is None:
            return modified, size, False
        
        if modified > last_modified or size != last_size:
            return modified, size, True
        
        return modified, size, False
    except FileNotFoundError:
        return None, None, False

def compare_files(original, modified, context_lines=16):
    """Compare original and modified files using the cs_diff tool."""
    script_dir = os.path.dirname(os.path.realpath(__file__))
    cs_diff_path = os.path.join(script_dir, "cs_diff.py")
    
    if not os.path.isfile(cs_diff_path):
        print(f"Error: cs_diff.py not found at {cs_diff_path}")
        return False
    
    try:
        cmd = [sys.executable, cs_diff_path, original, modified, "--context", str(context_lines)]
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error comparing files: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Monitor changes to Logic Pro controller assignment file')
    parser.add_argument('--interval', '-i', type=float, default=1.0, 
                        help='Polling interval in seconds (default: 1.0)')
    parser.add_argument('--output-dir', '-o', 
                        help='Directory to save snapshots of changed files')
    parser.add_argument('--no-diff', action='store_true',
                        help='Disable diff output when changes are detected')
    args = parser.parse_args()
    
    cs_file = get_cs_file_path()
    
    if not os.path.isfile(cs_file):
        print(f"Error: Logic Pro controller assignment file not found at {cs_file}")
        print("Make sure Logic Pro is installed and has been run at least once.")
        return 1
    
    print(f"Monitoring: {cs_file}")
    print("Make changes in Logic Pro's Controller Assignments window and save them.")
    print("Press Ctrl+C to stop monitoring.")
    
    # Create a temporary directory to store snapshots
    temp_dir = None
    if not args.output_dir:
        temp_dir = tempfile.mkdtemp(prefix="logic_cs_monitor_")
        output_dir = temp_dir
    else:
        output_dir = args.output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Take initial snapshot
        snapshot_path = os.path.join(output_dir, "cs_initial.bin")
        shutil.copy2(cs_file, snapshot_path)
        print(f"Initial snapshot saved to: {snapshot_path}")
        
        last_modified, last_size = os.stat(cs_file).st_mtime, os.stat(cs_file).st_size
        counter = 1
        
        while True:
            time.sleep(args.interval)
            
            modified, size, changed = file_has_changed(cs_file, last_modified, last_size)
            if changed:
                print(f"\n[{time.strftime('%H:%M:%S')}] Detected changes to controller assignment file!")
                
                # Save a new snapshot
                snapshot_path = os.path.join(output_dir, f"cs_snapshot_{counter}.bin")
                shutil.copy2(cs_file, snapshot_path)
                print(f"Snapshot saved to: {snapshot_path}")
                
                # Compare with previous snapshot
                if not args.no_diff:
                    prev_snapshot = os.path.join(output_dir, "cs_initial.bin" if counter == 1 else f"cs_snapshot_{counter-1}.bin")
                    print("\nChanges detected:")
                    compare_files(prev_snapshot, snapshot_path)
                
                last_modified, last_size = modified, size
                counter += 1
    
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
    finally:
        if temp_dir:
            print(f"\nTemporary snapshots are in: {temp_dir}")
            print("These will be deleted when you delete the directory.")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())