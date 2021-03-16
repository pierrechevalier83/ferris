Meet Ferris, a minimalistic keyboard
====================================

Named after the Rustlang mascott, Ferris is a 34 keys split keyboard that tries to be about as cute as its namesake.

![Ferris](https://i.imgur.com/TCjkquR.jpg)

Ferris is minimalistic: it aims to be a functional, ergonomic keyboard that is pleasing to use as a daily driver. It only supports choc keyswitches, although it would be easy to make a MX version if there was interest.

It is fully Open-Source: the kicad files are released under [the solderpad license, version 2.1](LICENSE). The firmware, contributed to [the QMK project](https://github.com/qmk/qmk_firmware/) is released under the GPL.
The Ferris 0.1 is certified by the Open Source Hardware.
![OSHWA](https://imgur.com/917TZru)

Status
------

| ![Validate ninja build file](https://github.com/pierrechevalier83/ferris/workflows/Validate%20ninja%20build%20file/badge.svg) | ![Format python code](https://github.com/pierrechevalier83/ferris/workflows/Format%20python%20code/badge.svg) |
|--|--|

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

Versions and variants
-----------------

There are currently two versions of the Ferris:
* [v0.1](0.1/readme.md) used an atmega32u4 microcontroller.
    * [Base variant](0.1/base/readme.md) (Choc switches with MX spacing)
    * [Ferris Low](0.1/low/readme.md) (Choc mini)
    * [Ferris High](0.1/high/readme.md) (MX switches)
    * [Ferris Compact](0.1/compact/readme.md) (Choc switches with choc spacing)
* [v0.2](0.2/readme.md) is in advanced prototyping stage and uses an Arm chip (STM32F072CBT6) which is more capable and cheaper than the atmega32u4. v0.2 also adds better ESD protection. The plan for v0.2 is to eventually offer full rust firmware as an alternative to qmk.
    * [Ferris Bling](0.2/bling/readme.md) (Choc, Choc spacing, packed with features)
    * [Ferris Compact](0.2/compact/readme.md) (Choc, Choc spacing, as minimalistic as the previous Ferris we all know and love)
    * [Ferris High](0.2/high/readme.md) (MX switches)
    * [Ferris Mini](0.2/mini/readme.md) (Choc mini switches with choc spacing)

How do I print one?
-------------------

Before you print one yourself, you're welcome contact the owner of this repository and see if they have spare boards to sell.

If they don't, or you prefer to have the full experience yourself,

* Decide which variant/version you want to print (refer to individual readme files in subdirectories for a short description of each variant).
* Download the `{version}.{variant}.release.zip` file from the latest [GitHub release on this repo](https://github.com/pierrechevalier83/ferris/releases/).

For a given version, you will find a release in this repository containing a zip file with the gerber files. This should be ready to send to a PCB manufacturer for assembly.
The repository also contains a bill of materials (bom.csv) with a list of the components you need and their reference number on LCSC.com. You may use another vendor for the components, as long as you make sure to get components that are equivalent.

How do I assemble one?
----------------------

The zip files for each release contain a file named `ibom.html`.

Open this file in a web browser for the variant you are building. It contains all the information needed to assemble
a keyboard, and is able to present it nicely in a contextual manner.

A few tips:
* Be mindful of the orientation of components.
	* The interactive bom has an option to "highlight first pin". TYou should match the pin drawn on the component to the side of the PCB that is highlighted. For a diode, the "first pin" is indicated with the cathode bar.
* You can change the order in which the components are displayed by clicking the column headers.
    * I like to sort the components by decreasing quantity to start with the most tedious work and end with the fun :)
* Most of the components are SMD mounted and can be soldered with a soldering iron, solder wire and flux (optional but strongly recomended).
    * If you are assembling a Ferris 0.2 - Bling, you will need a hot air station to place the LED driver chip.

And here are some key pieces of advice about soldering from my experience assembling many Ferris keyboards.
* If possible, use a wedge tip or other tip with a large enough surface. Pointy tips are harder, especially for drag soldering as they don't deliver as much heat at once.
* Don't use too much solder or you will have to wick it away and start again.
  * This especially applies to the USB C area and the small chips.
* Don't be shy on the flux: it really helps the solder flow where it should and keep away from surfaces it shouldn't go to.
* Don't use too much heat to avoid damaging the components. I've had good results with 350C for unleaded rosin core solder wire.
* Don't touch any component for too long with the iron to avoid heat damage. If you're not getting it right in a few seconds, let it cool down add more flux and try again. 
* Be sure to test every diode is properly soldered before soldering on the switches as the diodes are located under the switches and won't be accessible later on.

I took many pictures while building a Ferris 0.1 base variant.
The build log is here and may be of help:
Part 1:
[build log, part 1](https://imgur.com/gallery/jYbxkxE)
Part 2:
[build log, part 2](https://imgur.com/gallery/gs19F6E)

Where is the firmware?
----------------------

## QMK

The Ferris keyboard is powered by QMK as its main firmware.
The default keymap showcases one possible way to make a 34 keys keyboard usable and is documented [in its readme upstream](https://github.com/qmk/qmk_firmware/tree/master/keyboards/ferris/keymaps/default).
Firmware for v0.1 and the [Sweep](https://github.com/davidphilipbarr/Sweep) is already available [upstream](https://github.com/qmk/qmk_firmware/tree/master/keyboards/ferris).
Support for v0.2 should land upstream pretty soon with [this PR](https://github.com/qmk/qmk_firmware/pull/12133)
	- Support for the underglow feature is missing from this PR, but will come in a subsequent PR. It works for me locally :)

## ZMK

Support for v0.2 is also coming to upstream zmk with [this PR](https://github.com/zmkfirmware/zmk/pull/642)

## Rust firmware

I plan to write rust firmware for the v0.2 variants of the Ferris, eventually. Progress will be tracked in [this issue](https://github.com/pierrechevalier83/ferris/issues/2)


Automation
---

The philosophy of designing many simple keyboards rather than one versatile one which is slightly less good for any set of features results in an explosion in the number of designs one has to maintain.

## GitHub Actions

The keep this manageable, I have automated a number of steps such as [checking the Design Rules and the Electrical Rules](https://github.com/pierrechevalier83/ferris/actions/workflows/ci.yml) for each PCB on every commit push, and [generating release artifacts](https://github.com/pierrechevalier83/ferris/actions/workflows/release.yml) when a tag is pushed.

## Manually running within docker

Because GitHub actions perform these steps automatically, you shouldn't need to make use of the build system yourself, but for maintainers or curious bystanders, here is the workflow:

```
./automation/configure.py
```
Will generate a file named `build.ninja` in the root of the repository.

Then, running:
```
./automation/ninja.sh
```
will run `ninja` in [the ferris_automation docker container](https://hub.docker.com/repository/docker/pierrechevalier83/ferris_automation) which I published to dockerhub. This means minimal local setup is needed (basically, make sure you are able to run docker) as the specific tools are already contained in that docker image.
This will produce all build and release artifacts in a local directory called `build`.

## Running on the local system

If for a reason or another, you would prefer to run all of the tools locally rather than in `docker`, you may read the [ferris_automation Dockerfile](automation/Dockerfile) for inspiration and install the same software with the steps that work best on your platform.
In that case, docker will still be needed for some steps as it ensured [`kicad_cli`](https://github.com/pierrechevalier83/kicad_cli) can do its hackish UI manipulation in a known environment.

## Updating the `ferris_automation` docker image

When some of the scripts change in a way that will affect the `ferris_automation` docker container, I need to publish a new version.
This could be done as a GitHub action, but for now it is done manually with the following steps:

From the repo root:
```
docker build -t pierrechevalier83/ferris_automation:latest automation
docker push pierrechevalier83/ferris_automation:latest
```


