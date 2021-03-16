# PcbDraw-Lib

Model library for [PcbDraw](https://github.com/yaqwsx/PcbDraw) - tool for
creating awesome looking PCB drawings.

## Usage

Clone the repository to your computer and specify one of the directories as a
library when using PcbDraw. Currently there following libraries:

- `KiCAD-base` - module library in a standard style for components from KiCAD
  standard libraries.
- `Eagle-export` - module library in a standard style for components on imported
  Eagle boards. This library is held separately as the import of Eagle boards to
  KiCAD looses library information and component names do not follow KiCAD
  conventions.

## Creating Modules

Module is an SVG file containing a single component drawing. The file has to
follow these rules:

- it uses only SVG default units.
- one default unit corresponds to 1 mm in reality.
- it contains one element with `id=origin` having attributes `x` and `y`. Its
  coordinates serve as a module origin.
- origin should be a red rectangle of size 1x1.
- modules should not be too simplified (for example it is not OK for LED to be
  just a color circle).
- module is named exactly the same as the corresponding KiCAD footprint. The
  extension is changed to `.svg`.
- for each module there is a corresponding drawing with suffix '.back.svg' (for
  'pinheader.svg' there is a 'pinheader.back.svg'). This drawing contains view
  of the module from the other side of the board.
- each component should be placed on a tight canvas. The canvas size determines
  the highlighted area in component highlight.

Modules are placed in directories corresponding to KiCAD footprint libraries. If
multiple footprints are represented using one module, the module should not be
duplicated but symlinked.

Directory `scripts` contains script for automatic generation of modules - e.g.
pin headers, DIP packages, QFN packages, etc...

Side note: reasoning behind units and origin. Even SVG format supports unit and
origin can be placed at SVG (0,0) point, it not that easy in practice. Most of
the editors do weird things with coordinate system. Inkscape, for example,
reverses Y-axis and translates the origin by the initial size of document. When
you change the size of the document, the coordinates are not modified. Therefor,
I find placing origin component as the simplest solution which should be
compatible with any editor.

## Contributing

Please, help to increase usability of PcbDraw by adding more modules to the
library. Feel free to submit a pull request with new modules.
