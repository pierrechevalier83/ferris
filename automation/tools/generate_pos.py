#!/usr/bin/env python
#
# Generate a minimal pos file to serve as input to the jlc plugin
#
import pcbnew
import sys

board = pcbnew.LoadBoard(sys.argv[1])

MODULE_ATTR_NORMAL = 0
MODULE_ATTR_NORMAL_INSERT = 1
MODULE_ATTR_VIRTUAL = 2

print("Ref,PosX,PosY,Rot,Side")
for module in board.GetModules():
    if module.GetAttributes() == MODULE_ATTR_NORMAL_INSERT:
        (pos_x, pos_y) = module.GetPosition()
        side = "top"
        if module.IsFlipped():
            side = "bottom"
        data = {
            "Ref": module.GetReference(),
            "PosX": pos_x / 1000000.0,
            "PosY": pos_y / 1000000.0,
            "Rot": module.GetOrientation() / 10.0,
            "Side": side,
        }
        print('"{0[Ref]}",{0[PosX]},{0[PosY]},{0[Rot]},{0[Side]}'.format(data))
