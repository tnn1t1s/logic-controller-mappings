#\!/usr/bin/env python3
"""
Logic Pro Controller Assignment Decoder
---------------------------------------
This script attempts to decode Logic Pro's controller assignment file format
(com.apple.logic.pro.cs).

Initial findings:
- File starts with 'MROF' (FORM in little-endian) followed by 'FCSS  SG'
- Contains 'RGSC' markers at regular intervals (176 bytes apart)
- Contains many OSC-style paths (/softubeosd/...)
- Contains readable controller names and device information
"""

import os
import sys
import binascii
import struct
import argparse
from pathlib import Path
import re
import json

def get_strings_from_data(data, min_length=4):
    """Extract readable strings from binary data"""
    strings = []
    pattern = f'[A-Za-z0-9][A-Za-z0-9 ._-]{{{min_length-1},}}'.encode('ascii')
    for match in re.finditer(pattern, data):
        s = match.group(0).decode('ascii', errors='replace')
        if '?' not in s:  # Filter out strings with replacement characters
            strings.append((match.start(), s))
    return strings

def get_osc_paths_from_data(data):
    """Extract OSC-style control paths from binary data"""
    osc_patterns = []
    for match in re.finditer(b'/[A-Za-z0-9]+(/[A-Za-z0-9_]+)+', data):
        osc_patterns.append((match.start(), match.group(0).decode('ascii', errors='replace')))
    return osc_patterns

def decode_cs_file(filepath, output_format='text'):
    """
    Decode a Logic Pro controller assignment (.cs) file
    
    Parameters:
    - filepath: Path to the .cs file
    - output_format: 'text' or 'json'
    
    Returns:
    - Decoded information as string (text) or dict (json)
    """
    with open(filepath, 'rb') as f:
        data = f.read()
    
    # Basic file info
    file_info = {
        'filepath': filepath,
        'filesize': len(data),
        'header': binascii.hexlify(data[:16]).decode('ascii'),
    }
    
    # Extract file structure markers
    markers = {
        'FORM': data[:4] == b'MROF',
        'FCSS': data[8:12] == b'FCSS',
        'RGSC_count': len([m.start() for m in re.finditer(b'RGSC', data)]),
    }
    
    # Extract controller names and device info
    strings = get_strings_from_data(data)
    controller_info = []
    device_patterns = [
        'Logic Control', 'Logic Remote', 'Console 1',
        'Launchpad', 'TouchOSC', 'microKONTROL'
    ]
    
    for pos, s in strings:
        for pattern in device_patterns:
            if pattern in s:
                controller_info.append({
                    'offset': pos,
                    'name': s,
                    'type': pattern
                })
                break
    
    # Extract OSC paths which likely represent mappings
    osc_paths = get_osc_paths_from_data(data)
    mappings = []
    for pos, path in osc_paths:
        # Look for nearby strings that might be parameter names
        nearby_strings = []
        for s_pos, s in strings:
            if abs(s_pos - pos) < 100 and s not in path:
                nearby_strings.append(s)
        
        mapping = {
            'offset': pos,
            'path': path,
            'nearby_context': nearby_strings[:3] if nearby_strings else []
        }
        mappings.append(mapping)
    
    # Prepare result
    result = {
        'file_info': file_info,
        'markers': markers,
        'controllers': controller_info,
        'mappings': mappings[:100],  # Limit to first 100 for readability
    }
    
    if output_format == 'json':
        return result
    else:
        # Text output
        output = []
        output.append(f"File: {filepath}")
        output.append(f"Size: {len(data)} bytes")
        output.append(f"Header: {file_info['header']}")
        output.append("")
        
        output.append("File Structure:")
        output.append(f"  FORM marker (little-endian): {'Yes' if markers['FORM'] else 'No'}")
        output.append(f"  FCSS marker: {'Yes' if markers['FCSS'] else 'No'}")
        output.append(f"  RGSC block count: {markers['RGSC_count']}")
        output.append("")
        
        output.append("Detected Controllers:")
        for ctrl in controller_info:
            output.append(f"  {ctrl['name']} (at offset 0x{ctrl['offset']:x})")
        output.append("")
        
        output.append("Sample OSC Control Paths:")
        for i, mapping in enumerate(mappings[:30]):
            output.append(f"  {i+1}. {mapping['path']} (at offset 0x{mapping['offset']:x})")
            if mapping['nearby_context']:
                output.append(f"     Context: {', '.join(mapping['nearby_context'])}")
        
        return '\n'.join(output)

def main():
    parser = argparse.ArgumentParser(description='Decode Logic Pro controller assignment (.cs) files')
    parser.add_argument('filepath', help='Path to the .cs file to decode')
    parser.add_argument('--json', action='store_true', help='Output in JSON format')
    parser.add_argument('--output', '-o', help='Write output to file instead of stdout')
    args = parser.parse_args()
    
    if not os.path.isfile(args.filepath):
        print(f"Error: File not found: {args.filepath}")
        return 1
    
    output_format = 'json' if args.json else 'text'
    result = decode_cs_file(args.filepath, output_format)
    
    if args.output:
        with open(args.output, 'w') as f:
            if output_format == 'json':
                json.dump(result, f, indent=2)
            else:
                f.write(result)
        print(f"Output written to {args.output}")
    else:
        if output_format == 'json':
            print(json.dumps(result, indent=2))
        else:
            print(result)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
