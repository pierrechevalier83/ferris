Ferris 0.1
===

![Ferris 0.1 family](https://i.imgur.com/TCjkquR.jpg)

The 0.1 variants of the Ferris generally share the same underlying PCB design,
with varying functionalities to cater to different tastes.

The left hand uses an Atmega32u4 chip with an external crystal connected to the
computer via USB-C.

The right hand is connected to the left hand using a 4 poles TRRS Jack cable.
On the right PCB, there is a passive I/O expander (the MCP23017) which allows to
handle the input from the 5 by 4 switch matrix while only needing 4 pins (for i2c)
between halves.

Four variants were designed, printed and verified to work:
* [Base variant](base/readme.md) (Choc switches with MX spacing)
* [Ferris Low](low/readme.md) (Choc mini)
* [Ferris High](high/readme.md) (MX switches)
* [Ferris Compact](compact/readme.md) (Choc switches with choc spacing)

Note that the 0.1 design does not include any protection against electrostatic discharge.

For that reason, it is recommended to favour the 0.2 designs except if you really prefer
one of the 0.1 variants for some specific reason (for instance, you may have spare
Atmega32u4 chips on hand).
