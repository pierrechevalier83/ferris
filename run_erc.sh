#!/bin/bash
ERC_OUTPUT=$(docker run --rm -t -e VARIANT=$1 -e RUST_LOG -v "$(pwd)":/workdir pierrechevalier83/kicad_cli bash -c 'RUSTLOG=$RUSTLOG kicad_cli run-erc $VARIANT/ferris.sch --headless')

if [[ -z "$ERC_OUTPUT" ]]; then
	echo -e "\e[1;32mERROR\e[0m"
	echo "Missing ERC report line. Something went wrong"
	exit 2
else
	if [[ "$ERC_OUTPUT" == "ErcOutput { num_errors: 0, num_warnings: 0 }"* ]]; then
		echo -e "\e[1;32mPASS\e[0m"
		echo "$ERC_OUTPUT"
	    exit 0
	else
		echo -e "\e[1;32mFAIL\e[0m"
		echo "$ERC_OUTPUT"
		exit 1
	fi
fi
