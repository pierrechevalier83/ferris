#!/usr/bin/env python

"""
Generates pin header in KiCAD style from a single pin model.
Models are generated in current working directory.
"""

from lxml import etree
from copy import deepcopy
import argparse 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("model", help="Single pin header model. Group with id 'pin' has to be present.");
    parser.add_argument("file_template", help="Python formatting string for name of the models.")

    args = parser.parse_args()

    document = etree.parse(args.model)
    root = document.getroot()
    pin = root.find(".//*[@id='pin']")
    for i in range(1, 40):
        el = deepcopy(pin)
        del el.attrib["id"]
        el.attrib["transform"] = "translate(0 {})".format(i * 2.54)
        root.append(el)
        document.write(args.file_template.format(i + 1))