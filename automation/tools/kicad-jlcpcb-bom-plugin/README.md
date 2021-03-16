# KiCad JLCPCB BOM Plugin

Export a JLCPCB Compatible BOM directly from your KiCad schematic!

## Installation

This script requires **Python 3**. If you need a Python 2 version, please get
[kicad-jlcpcb-bom-plugin version 1.0.0](https://github.com/wokwi/kicad-jlcpcb-bom-plugin/releases/tag/1.0.0) instead.

The script has been tested with KiCad 5.1.4.

1. Copy `bom_csv_jlcpcb.py` to your KiCad installation folder under the `bin/scripting/plugins` directory
2. In Eschema (the Schematics editor) go to "Tools" -> "Generate Bill of Materials", press the "+" button 
   at the bottom of the screen, and choose the plugin file you have just copied. When asked for a nickname,
   go with the default, "bom_csv_jlcpcb".

## Usage

Instructions for exporting JLCPCB BOM from KiCad's Eschema:

1. Go to "Tools" -> "Generate Bill of Materials"
2. Choose "bom_csv_jlcpcb" from the "BOM plugins" list on the left
3. Make sure the command line ends with "%O.csv" (otherwise, change "%O" into "%O.csv")
4. Click on "Generate". The BOM file should be created inside your project's directory, as a CSV file.

## Custom Fields

You can customize the script's output by adding the following fields to your components:

1. "LCSC Part" - Add this field to include an LCSC Part number in the generated BOM. e.g.: C2286 for a red LED.
2. "JLCPCB BOM" - Set this field to 0 (or "False") to omit the component from the generated BOM.

## Generating a JLCPCB CPL File

You can use the `kicad_pos_to_cpl.py` script to convert a KiCad Footprint Position (.pos) file into a CPL file
compatible with JLCPCB SMT Assembly service. The `.pos` file can be generated from Pcbnew, by going into 
"File" -> "Fabrication Outputs" -> "Footprint Position (.pos) File..." and choosing the following options:

* Format: CSV
* Units: Millimeters
* Files: Separate files for front and back

Also, make sure to uncheck "Include footprints with SMD pads even if not marked Surface Mount". 

