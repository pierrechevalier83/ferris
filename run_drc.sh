DRC_OUTPUT=$(docker run --rm -t -v "$(pwd)"/$1:/kicad-project productize/kicad-automation-scripts python -m kicad-automation.pcbnew_automation.run_drc /kicad-project/ferris.kicad_pcb "$(pwd)"/build | grep "INFO:root" | sed "s/INFO:root//")

if [[ -z "$DRC_OUTPUT" ]]; then
	echo -e "\e[1;32mERROR\e[0m"
	echo "Missing ERC report line. Something went wrong"
	exit 2
else
	if [[ "$DRC_OUTPUT" = *"'drc_errors': 0, 'unconnected_pads': 0"* ]]; then
		echo -e "\e[1;32mPASS\e[0m"
		echo "$DRC_OUTPUT"
	    exit 0
	else
		echo -e "\e[1;32mFAIL\e[0m"
		echo "$DRC_OUTPUT"
		exit 1
	fi
fi
