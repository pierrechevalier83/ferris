#!/usr/bin/env bash

for i in `find . -name '*.svg'`; do echo "Processing $i"; inkscape --verb=FitCanvasToDrawing --verb=FileSave --verb=FileClose --verb=FileQuit $i ; done