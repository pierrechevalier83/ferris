#!/bin/bash
if [[ -z "$WORKDIR" ]]; then
	export WORKDIR="$(pwd)";
fi
VARIANT=$1

# Try 5 times as it sometimes fails
for attempt in {0..5}
do
    docker run --user $(id -u $USER):$(id -g $USER) -e VARIANT=$VARIANT -v $WORKDIR:/workdir -t pierrechevalier83/ferris_automation bash -c 'echo ${VARIANT} && Xvfb :98 & python3 tools/InteractiveHtmlBom/InteractiveHtmlBom/generate_interactive_bom.py $VARIANT/ferris.kicad_pcb --dest-dir ../../build/$VARIANT --netlist-file $VARIANT/ferris.xml --extra-fields "LCSC Part" --dnp-field "DNP" --no-browser' && exit 0
done
exit 1
