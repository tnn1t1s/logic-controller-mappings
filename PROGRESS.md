# Progress Report: Investigating Logic's `com.apple.logic.pro.cs` File Format

This document summarizes the progress made on investigating and documenting Logic Pro's controller assignment file format as outlined in Issue #1.

## Initial Findings

### File Format Structure

- **Header**: The file begins with `MROF` (which is "FORM" in little-endian) followed by `FCSS  SG`
- **Block Structure**: Contains recurring `RGSC` markers at regular intervals (typically 176 bytes apart)
- **File Size**: The sample file analyzed was 425,760 bytes
- **Block Count**: Found 20 `RGSC` blocks in the sample file

### Readable Content

- **Controller Names**: The file contains human-readable names of controllers (e.g., "Logic Control", "Console 1", "TouchOSC")
- **OSC Paths**: Many OSC-style paths are present, following patterns like:
  - `/softubeosd/volume/0`
  - `/softubeosd/pan/0`
  - `/softubeosd/send1/0`
  - These likely represent parameter mappings

### Mapping Structure

Based on the OSC paths found and their nearby context, mappings seem to follow a pattern:
- Parameter name (e.g., `volume_0`)
- OSC path for the parameter (e.g., `/softubeosd/volume/0`)
- Additional paths for value representation (e.g., `/softubeosd/volume_val/0`)
- Modifiers for the mapping (e.g., `/softubeosd/volume/0/z`)

## Tools Developed

To aid in the investigation, the following tools have been created:

1. **cs_analyzer.py**: A basic analysis tool that:
   - Reports file size and header information
   - Finds and counts recurring markers
   - Extracts human-readable strings
   - Identifies OSC-style control paths

2. **cs_diff.py**: A comparison tool that:
   - Compares two `.cs` files to identify binary differences
   - Shows context around changes
   - Helps in understanding what changes when mappings are modified

3. **cs_monitor.py**: A real-time monitoring tool that:
   - Watches for changes to the `.cs` file as mappings are created/modified
   - Saves snapshots of the file at each change point
   - Automatically compares versions to highlight changes

4. **decode_logic_cs.py**: A decoder that:
   - Analyzes the file structure
   - Extracts controller information
   - Lists OSC control paths with context
   - Outputs results in text or JSON format

## Next Steps

To complete the investigation, the following steps are recommended:

1. **Controlled Testing**:
   - Create a "clean" Logic project without any controller assignments
   - Add mappings one by one, monitoring changes after each addition
   - Document the structure changes for each mapping type (button, knob, fader)

2. **Format Documentation**:
   - Create a comprehensive document describing the file format
   - Include details on the header, block structure, and mapping format
   - Document where controller names, parameter names, and values are stored

3. **Mapping Extraction**:
   - Develop a tool to extract existing mappings from a `.cs` file
   - Create a format for representing mappings in a human-readable format (JSON/YAML)

4. **Mapping Creation**:
   - Research whether it's possible to create new mappings and inject them into the file
   - Test modifying existing mappings to determine what validation Logic does

## Conclusion

The initial investigation has yielded valuable insights into Logic Pro's controller assignment file format. The tools developed will facilitate further research and potentially enable portable, shareable controller mappings in the future.

This work directly supports the project's goal of making Logic Pro's controller mappings more open and modular.