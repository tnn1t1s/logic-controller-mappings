# Background

Logic Pro allows controller assignments through its Controller Assignments window, but stores them in a proprietary binary format: `~/Library/Preferences/com.apple.logic.pro.cs`.

These mappings:
- Are hard to edit manually
- Are tied to specific plugin instances and tracks
- Cannot be exported or shared cleanly across systems

Softube Console 1 provides a hardware+software experience with pre-mapped controls for channel strip plugins. We believe this should be replicable with generic MIDI controllers and shared templates.

This repo is an effort to reverse engineer and standardize that workflow, even if Apple hasn't made it easy.

