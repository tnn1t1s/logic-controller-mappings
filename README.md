# Logic Plugin Controller Mapping Project

This is an open project by Abril Studios to explore and document how to map common MIDI controllers to plugin parameters in Logic Pro—especially for recreating workflows like Softube Console 1 without being locked into proprietary hardware.

We believe controller mappings should be portable, editable, and artist-owned.

## Project Goals

- Decode Logic Pro's controller mapping format
- Build reusable templates for common plugin strips (SSL, API, Neve, etc.)
- Allow generic MIDI controllers to act like Console 1-style surfaces
- Release open tools to facilitate mapping and sharing

## Progress Update

We've started work on decoding Logic Pro's controller assignment file format (`com.apple.logic.pro.cs`). Initial investigation has revealed:

- The file has a structured binary format with identifiable markers
- It contains readable controller names and OSC-style control paths
- Mappings appear to follow consistent patterns

We've created several tools to aid in the investigation:
- `src/decode_logic_cs.py`: Main decoder for the CS file format
- `tools/cs_analyzer.py`: Basic structural analysis tool
- `tools/cs_diff.py`: Compares different versions of CS files
- `tools/cs_monitor.py`: Monitors CS file changes in real-time

For detailed findings, see the [PROGRESS.md](PROGRESS.md) document.

## Getting Started

1. Clone this repository
2. Back up your existing controller assignments file:
   ```bash
   cp ~/Library/Preferences/com.apple.logic.pro.cs ./samples/my_backup.cs
   ```
3. Run the decoder to analyze your file:
   ```bash
   python3 src/decode_logic_cs.py ./samples/my_backup.cs
   ```

## Controller Mappings

We are developing standardized mappings for popular MIDI controllers:

- [Korg nanoKONTROL2](controllers/nanokontrol2/) - For SSL Channel Strip

## Contributing

This is an open research project. If you'd like to contribute, please check the [CONTRIBUTING.md](CONTRIBUTING.md) guide and look at open issues.
