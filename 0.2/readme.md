Ferris 0.2
===

![Ferris Bling](https://i.imgur.com/LwKlmnz.jpg)
![Ferris Bling Silk](https://media4.giphy.com/media/7GF1Ns1y66IMlpD9lN/giphy.gif)

The 0.2 variants of the Ferris generally share the same hardware, although the
Ferris bling has additional circuitry to offer RGB underglow.

Like the 0.1 designs, multiple variants are available to cater for different tastes.

The left hand uses an arm chip (STM32F072) as well as components to protect the board
against electrostatic discharge.

The right hand is connected to the left hand using a 4 poles TRRS Jack cable.
On the right PCB, there is a passive I/O expander (the MCP23017) which allows to
handle the input from the 5 by 4 switch matrix while only needing 4 pins (for i2c)
between halves.

Four variants were designed. Not all were tested yet. See subdirectories for individual
status
* [Ferris Bling](bling/readme.md) (Choc, Choc spacing, packed with features)
* [Ferris Compact](compact/readme.md) (Choc, Choc spacing, as minimalistic as the previous Ferris we all know and love)
* [Ferris High](high/readme.md) (MX switches)
* [Ferris Mini](mini/readme.md) (Choc mini switches with choc spacing)

If there is a combination of features that you are interested in and none of these variants offer,
feel free to raise an issue or a PR :)
