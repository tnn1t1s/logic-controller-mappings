# Controller Mappings

This directory contains documentation and mapping templates for different MIDI controllers used in the project.

## Available Controllers

- [Korg nanoKONTROL2](nanokontrol2_mapping.md) - Default mapping reference for the Korg nanoKONTROL2

## Mapping Format

Each controller will have:

1. A documentation file (`.md`) describing the controller's default MIDI implementation
2. A mapping template (`.json`) that can be applied to Logic Pro's controller assignment file

## How to Use

1. Find your controller in the list above
2. Review the default MIDI implementation
3. Use the mapping tools to apply the controller template to your Logic Pro setup

## Contributing

To add a new controller, please create:

1. A markdown documentation file with the controller's default MIDI implementation
2. A JSON mapping template that follows our schema (see [CONTRIBUTING.md](../CONTRIBUTING.md))
3. Update this README to include your controller in the list