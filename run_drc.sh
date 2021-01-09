#!/bin/bash
DRC_OUTPUT=$(docker run --rm -t -e VARIANT=$1 -e RUST_LOG -v "$(pwd)":/workdir pierrechevalier83/kicad_cli bash -c 'kicad_cli run-drc $VARIANT/ferris.kicad_pcb --headless')

if [[ -z "$DRC_OUTPUT" ]]; then
	echo -e "\e[1;32mERROR\e[0m"
	echo "Missing DRC report line. Something went wrong"
	echo "$FULL_DRC_OUTPUT"
	exit 2
else
	if [[ "$DRC_OUTPUT" == "DrcOutput { num_errors: 0, num_unconnected_pads: 0 }"* ]]; then
		echo -e "\e[1;32mPASS\e[0m"
		echo "$DRC_OUTPUT"
	    exit 0
	else
		echo -e "\e[1;32mFAIL\e[0m"
		echo "$DRC_OUTPUT"
		exit 1
	fi
fi
