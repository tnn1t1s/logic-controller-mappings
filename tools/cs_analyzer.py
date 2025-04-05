#!/usr/bin/env python3
"""
Logic Pro Controller Assignment Analyzer
---------------------------------------
This script analyzes the com.apple.logic.pro.cs file which stores
Logic Pro's controller assignments.
"""

import os
import sys
import binascii
import struct
import argparse
from pathlib import Path
import re

def analyze_cs_file(filepath):
    """Analyze the structure of a .cs file"""
    with open(filepath, 'rb') as f:
        data = f.read()
    
    print(f"File size: {len(data)} bytes")
    
    # Check header
    header = data[:16]
    header_hex = binascii.hexlify(header).decode('ascii')
    print(f"Header: {header_hex}")
    print(f"ASCII: {repr(header)}")
    
    # The file appears to start with "MROF" which is "FORM" backwards (little-endian)
    if data[:4] == b'MROF':
        print("Identified header: 'MROF' (FORM in little-endian)")
    
    # Look for "FCSS  SG" marker which appears at offset 8
    if data[8:16] == b'FCSS  SG':
        print("Identified marker: 'FCSS  SG' at offset 8")
    
    # Look for recurring "RGSC" markers which appear in the file
    rgsc_positions = [m.start() for m in re.finditer(b'RGSC', data)]
    print(f"Found {len(rgsc_positions)} instances of 'RGSC' marker")
    if rgsc_positions:
        print(f"First few positions: {rgsc_positions[:5]}")
        
        # Analyze the pattern/distance between markers
        if len(rgsc_positions) > 1:
            distances = [rgsc_positions[i+1] - rgsc_positions[i] for i in range(len(rgsc_positions)-1)]
            print(f"Distances between markers: {distances[:5]} ...")
    
    # Extract strings that might be controller names, parameter names, etc.
    strings = []
    for match in re.finditer(b'[A-Za-z0-9][A-Za-z0-9 ._-]{7,}', data):
        s = match.group(0).decode('ascii', errors='replace')
        if '?' not in s:  # Filter out strings with replacement characters
            strings.append((match.start(), s))
    
    print(f"\nFound {len(strings)} potential string values")
    print("\nSample strings:")
    for pos, s in sorted(strings)[:30]:
        print(f"  Offset {pos}: {s}")
    
    # Look for OSC patterns which might indicate mappings
    osc_patterns = []
    for match in re.finditer(b'/[A-Za-z0-9]+(/[A-Za-z0-9_]+)+', data):
        osc_patterns.append((match.start(), match.group(0).decode('ascii', errors='replace')))
    
    print(f"\nFound {len(osc_patterns)} potential OSC control paths")
    print("\nSample OSC paths:")
    for pos, s in sorted(osc_patterns)[:20]:
        print(f"  Offset {pos}: {s}")

def main():
    parser = argparse.ArgumentParser(description='Analyze Logic Pro controller assignment (.cs) files')
    parser.add_argument('filepath', help='Path to the .cs file to analyze')
    args = parser.parse_args()
    
    if not os.path.isfile(args.filepath):
        print(f"Error: File not found: {args.filepath}")
        return 1
    
    analyze_cs_file(args.filepath)
    return 0

if __name__ == '__main__':
    sys.exit(main())