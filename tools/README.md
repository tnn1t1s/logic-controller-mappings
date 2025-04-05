# Logic Controller Assignment File Analysis Tools

This directory contains tools for analyzing Logic Pro's controller assignment file format (`com.apple.logic.pro.cs`).

## Available Tools

### cs_analyzer.py

A basic tool for analyzing the structure of a Logic Pro controller assignment file.

```bash
python3 cs_analyzer.py /path/to/com.apple.logic.pro.cs
```

### cs_diff.py

Compares two controller assignment files to identify changes.

```bash
python3 cs_diff.py original.cs modified.cs
```

Options:
- `--context` or `-c`: Number of context bytes to show around differences (default: 16)

### cs_monitor.py

Monitors changes to Logic Pro's controller assignment file as you make changes in the Controller Assignments window.

```bash
python3 cs_monitor.py
```

Options:
- `--interval` or `-i`: Polling interval in seconds (default: 1.0)
- `--output-dir` or `-o`: Directory to save snapshots of changed files
- `--no-diff`: Disable diff output when changes are detected

## Workflow for Investigation

1. **Backup Your Current Settings**:
   ```bash
   cp ~/Library/Preferences/com.apple.logic.pro.cs ~/Desktop/original.cs
   ```

2. **Monitor Changes**:
   ```bash
   python3 tools/cs_monitor.py --output-dir ~/Desktop/cs_snapshots
   ```

3. **Make Controller Assignments in Logic Pro**:
   - Open Logic Pro
   - Open Controller Assignments (Menu: Logic Pro > Settings > Controller Assignments)
   - Make assignments
   - Save

4. **Analyze the Changes**:
   ```bash
   python3 tools/cs_diff.py ~/Desktop/cs_snapshots/cs_initial.bin ~/Desktop/cs_snapshots/cs_snapshot_1.bin
   ```

5. **Create Documentation**:
   Document patterns, structures, and any findings in the project wiki or documentation.

## File Format Findings

From initial analysis, we know:

- The file starts with "MROF" (FORM in little-endian) followed by "FCSS  SG"
- "RGSC" markers appear at regular intervals (usually 176 bytes apart)
- The file contains human-readable strings for controller names and device info
- Many OSC-style paths appear to be used for mappings (e.g., `/softubeosd/volume/0`)
- Controller assignments seem to follow a pattern with values and nearby context

Further investigation is needed to fully understand the format and develop a reliable decoder.