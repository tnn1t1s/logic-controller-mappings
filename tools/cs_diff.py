#!/usr/bin/env python3
"""
Logic Pro Controller Assignment Diff Tool
----------------------------------------
This script compares two com.apple.logic.pro.cs files to identify changes
between controller assignments.
"""

import os
import sys
import binascii
import argparse
from pathlib import Path
import re
import difflib

def hexdump(data, offset=0, length=16):
    """Generate a hexdump-like output of binary data"""
    result = []
    for i in range(0, len(data), 16):
        chunk = data[i:i+16]
        hex_values = ' '.join(f'{b:02x}' for b in chunk)
        ascii_values = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
        result.append(f"{offset+i:08x}  {hex_values:<47}  |{ascii_values}|")
    return '\n'.join(result)

def compare_cs_files(file1, file2, context_lines=3):
    """Compare two .cs files and show differences"""
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        data1 = f1.read()
        data2 = f2.read()
    
    print(f"File 1 size: {len(data1)} bytes")
    print(f"File 2 size: {len(data2)} bytes")
    
    if len(data1) != len(data2):
        print(f"Size difference: {len(data2) - len(data1)} bytes")
    
    # Compare files binary-wise and find difference locations
    differences = []
    for i, (b1, b2) in enumerate(zip(data1, data2)):
        if b1 != b2:
            differences.append(i)
    
    if not differences:
        print("Files are identical")
        return
    
    print(f"Found {len(differences)} byte differences")
    
    # Group differences into contiguous blocks
    blocks = []
    current_block = []
    for diff in differences:
        if not current_block or diff == current_block[-1] + 1:
            current_block.append(diff)
        else:
            blocks.append(current_block)
            current_block = [diff]
    if current_block:
        blocks.append(current_block)
    
    print(f"Differences grouped into {len(blocks)} blocks")
    
    # Show each difference block with context
    for i, block in enumerate(blocks):
        start = max(0, block[0] - context_lines)
        end = min(len(data1), block[-1] + context_lines + 1)
        
        print(f"\n=== Difference Block {i+1} ===")
        print(f"Offset range: 0x{block[0]:x} - 0x{block[-1]:x} (Length: {len(block)} bytes)")
        
        # Show surrounding strings that might provide context
        strings_near = []
        for pos in range(max(0, block[0]-100), min(len(data1), block[-1]+100)):
            # Look for readable string starting at this position
            if 32 <= data1[pos] < 127:  # Printable ASCII
                s = bytearray()
                for j in range(pos, min(pos + 50, len(data1))):
                    if 32 <= data1[j] < 127:
                        s.append(data1[j])
                    else:
                        break
                if len(s) >= 4:  # Only show strings of reasonable length
                    strings_near.append((pos, s.decode('ascii')))
        
        if strings_near:
            print("\nNearby strings:")
            for pos, s in strings_near[:5]:  # Show up to 5 nearby strings
                print(f"  Offset 0x{pos:x}: {s}")
        
        print("\nOld data:")
        print(hexdump(data1[start:end], offset=start))
        print("\nNew data:")
        print(hexdump(data2[start:end], offset=start))

def main():
    parser = argparse.ArgumentParser(description='Compare two Logic Pro controller assignment (.cs) files')
    parser.add_argument('file1', help='Path to the first (original) .cs file')
    parser.add_argument('file2', help='Path to the second (modified) .cs file')
    parser.add_argument('--context', '-c', type=int, default=16, help='Number of context bytes to show around differences (default: 16)')
    args = parser.parse_args()
    
    if not os.path.isfile(args.file1):
        print(f"Error: File not found: {args.file1}")
        return 1
    
    if not os.path.isfile(args.file2):
        print(f"Error: File not found: {args.file2}")
        return 1
    
    compare_cs_files(args.file1, args.file2, args.context)
    return 0

if __name__ == '__main__':
    sys.exit(main())