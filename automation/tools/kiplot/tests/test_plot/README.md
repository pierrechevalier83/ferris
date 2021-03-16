This directory contains tests for full testing of KiCad plots.
This tests:

* KiPlot's config parsing and driving of KiCad
* KiCad's own plotting code

Generally, boards are drawn from `../board_samples` and configs from
`yaml_samples`. Sometimes, the YAML samples are modified by the test
runners to avoid having hundreds of them!

Bug that should be tested for:

* https://bugs.launchpad.net/kicad/+bug/1775037