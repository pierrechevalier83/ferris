#!/usr/bin/env python3
# coding=utf8

# Converts a KiCad Footprint Position (.pos) File into JLCPCB compatible CPL file
# Copyright (C) 2019, Uri Shaked. Released under the MIT license.
# 
# Usage: kicad_pos_to_cpl.py <input.csv> <output.csv> [overrides.json]
#
# The overrides file is a JSON file that contains a single object. The key of that object
# is the reference of the part of override, and the value is the amount of degrees to
# add to the part's rotation. For instance, to rotate U1 by 90 degrees, and Q1 by 180
# degrees, put the following value in the overrides.json file:
# { "U1": 90, "Q1": 180 }

import sys
import csv
import json
from collections import OrderedDict

overrides = {}

if len(sys.argv) == 4:
    with open(sys.argv[3], 'r') as overrides_file:
        overrides = json.load(overrides_file)

with open(sys.argv[1], 'r') as in_file, open(sys.argv[2], 'w', newline='') as out_file:

    reader = csv.DictReader(in_file)
    ordered_fieldnames = OrderedDict([('Designator',None),('Mid X',None),('Mid Y',None),('Layer',None),('Rotation',None)])
    writer = csv.DictWriter(out_file, fieldnames=ordered_fieldnames)
    writer.writeheader()

    for row in reader:
        angle_adjustment = overrides.get(row['Ref'], 0)
        writer.writerow({
            'Designator': row['Ref'], 
            'Mid X': row['PosX'] + 'mm', 
            'Mid Y': row['PosY'] + 'mm', 
            'Layer': row['Side'].capitalize(), 
            'Rotation': (360 + int(float(row['Rot']) + angle_adjustment)) % 360
        })
