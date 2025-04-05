# Controller Mappings

This directory contains documentation and mapping templates for different MIDI controllers used in the project.

## Available Controllers

- [Korg nanoKONTROL2](nanokontrol2/) - Maps to SSL Channel Strip plugin

## Directory Structure

Each controller has its own subdirectory containing:

1. A `README.md` with documentation about the controller's default MIDI implementation
2. JSON mapping templates (e.g., `ssl_mapping_korg.json`) that define parameter mappings

## How to Use

1. Find your controller in the list above
2. Review its default MIDI implementation in the README.md
3. Use the JSON template as a basis for mapping to plugins in Logic Pro
4. Apply using the mapping tools (coming soon)

## Contributing

To add a new controller, please:

1. Create a directory with your controller's name (`controllers/your_controller_name/`)
2. Add a `README.md` with the controller's default MIDI implementation details
3. Create JSON mapping templates for supported plugins
4. Update this README to include your controller in the list

For more details, see the main [CONTRIBUTING.md](../CONTRIBUTING.md).