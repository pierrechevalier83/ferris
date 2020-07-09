Meet Ferris, a minimalistic keyboard
====================================

Named after the Rustlang mascott, ferris is a 34 keys split keyboard that tries to be about as cute as its namesake.

![Ferris](https://i.imgur.com/qOv4XDe.jpeg)

Ferris is minimalistic: it aims to be a functional, ergonomic keyboard that is pleasing to use as a daily driver. It only supports choc keyswitches, although it would be easy to make a MX version if there was interest.

It is fully Open-Source: the kicad files are released under [the solderpad license, version 2.1](LICENSE). The firmware, contributed to [the QMK project](https://github.com/qmk/qmk_firmware/) is released under the GPL.

Design philosophy
-----------------

The Ferris was designed around this set of goals:
* Comfort
* Aesthetics
* Portability
* Ease of assembly
* Low-Cost
* Low-Profile
* 34 keys
* Hackable
* USB-C
* No compromise

and this set of non-goals:
* Reversible PCB used for both hands
* Pro-micro/Elite C/Proton C support
* Hot-Swap support
* Multi-switches support
* Support for any feature (RGB, OLED, encoders, ...) that is not of interest to the user

You may read more about how each feature (and mostly lack thereof) contributes to these goals [in this write up](docs/design_philosophy.md) once described as "overly long and almost pretentious" :)

Technical details
-----------------

### Base variant, rev 0.1

This describes the first ever iteration of the Ferris keyboard: a plain pcb with support for choc switches, and the same layout as the Kyria (but limited to 34 keys).

* USB C
* 34 keys (3x5 + 2 thumb keys per hand)
* Split
* Atmega32u4 microcontroller on the left hand side
* MCP23017 on the right hand side
* A 4 poles jack cable carries data between halves using the i2c protocol
* The diodes live under the switches where they are snuggly hidden from sight
* No holes through the PCB. The intent is to use it case-less.
* Switches are spaced by 19mm from each other in each direction (almost exactly what's known as MX spacing [19.05x19.05]). This allows for a wider variety of compatible keycaps for the price of gaps for certain keycaps that respect the Kailh choc specification
* Columnar stagger identical to the one on the Kyria

### Upcoming changes

In rev 0.2, I would like to implement the following changes:

* Microcontroller: [Arm STM32F030F4P6TR](https://lcsc.com/product-detail/Others_STMicroelectronics_STM32F030F4P6TR_STMicroelectronics-STM32F030F4P6TR_C89040.html) instead of [Atmega32u4](https://lcsc.com/product-detail/ATMEL-AVR_ATMEL_ATMEGA32U4-AU_ATMEGA32U4-AU_C44854.html)
  * Cheaper: 0.83$ instead of $3.63, less unused pins, easier to solder, more flash, more ram, better rust support for possible pure rust firmware
* IO Expander: [PCA9539PW ](https://lcsc.com/product-detail/I-O-Expansion_NXP_PCA9539PW_PCA9539PW_C129516.html) instead of [MCP23017](https://lcsc.com/product-detail/Interface-ICs_MICROCHIP_MCP23017-E-SO_MCP23017-E-SO_C47023.html)
  * Cheaper 0.76$ instead of 1.56$
* Spacing: 0.18x0.19 instead of 0.19x0.19
  * Avoids gaps with keycaps that conform with the Kailh specifications
  * More ergonomic as fingers don't have to move as far up and down
  * Con: Looses compatibility to some keycaps
* Ferris MX:
  * I would like to also do a run with MX only footprints for anyone interested
* Ferris tent:
  * I would like to add four mounting holes on each hand to support the tenting puck that Thomas Baart at splitkb.com is currently designing

How to I print one?
-------------------

For a given version, you will find a release in this repository containing a zip file with the gerber files. This should be ready to send to a PCB manufacturer for assembly.
The repository also contains a bill of materials (bom.csv) with a list of the components you need and their reference number on LCSC.com. You may use another vendor for the components, as long as you make sure to get components that are equivalent.

How do I assemble one?
----------------------

Here is where the components go on the pcb:
![components around the microcontroller](https://i.imgur.com/DC6uJEx.png)
![components around the usb c and the io expander](https://i.imgur.com/zMLJDx9.png)

Most of these components are smd mounted. They can be soldered in with hot air and solder paste or with a soldering iron, solder wire and flux.
I have found it easier to control how much solder I use with a soldering iron.

Here are some key pieces of advice I can give from my experience assembling 3 of them so far:
* Be mindful of the orientation for the components that are polarized:
  * Diodes: cathode bar on the right side for both pcbs
  * Crystal: text readable looking at it from the controller
  * Controller: pin 1 dot indicator in the top right
  * IO expander: pin 1 dot indicator in the top left
* Use a wedge tip or other tip with a large enough surface. Pointy is harder.
* Don't use too much solder or you will have to wick it away and start again.
  * This especially applies to the USB C area and the microcontroller.
* Don't be shy on the flux: it really helps the solder flow where it should and keep away from surfaces it shouldn't go to.
* Don't use too much heat to avoid damaging the components. I've had good results with 350C for unleaded rosin core solder wire.
* Don't touch any component for too long with the iron to avoid heat damage. If you're not getting it right in a few seconds, let it cool down add more flux and try again. 
* Be sure to test every diode is properly soldered before soldering on the switches as the diodes are located under the switches and won't be accessible later on.
* I have found it easier to solder the crystal with hot air as it is hard to reach the solder from under it with an iron. Your mileage may vary

I took many pictures while building a board. If you want to build a Ferris while following along,
Part 1:
[build log, part 1](https://imgur.com/gallery/jYbxkxE)
Part 2:
[build log, part 2](https://imgur.com/gallery/gs19F6E)

Where is the firmware?
----------------------

For now, the Ferris keyboard is powered by QMK. Firmware for it is available [in this PR](https://github.com/qmk/qmk_firmware/pull/9634) and should make it upstream once the review process has taken its course.

The default keymap is very minimalistic. I will come up with something fancier in due time.

Status:
-------
v 0.1 is confirmed to work: I have printed 5 on jlcpcb.com and assembled 3. I have flashed the firmware on all of these and made sure that all keys are recognized as intended. I am also typing these words on a Ferris.

Here is a short demo of a working Ferris:
[typing test](https://i.imgur.com/E8Wipxz.mp4)
