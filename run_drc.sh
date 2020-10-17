# Super hacky: I'm replacing the timeout value in the docker container on the fly so it works with larger projects
FULL_DRC_OUTPUT=$(docker run --rm -t -v "$(pwd)"/$1:/kicad-project productize/kicad-automation-scripts bash -c 'sed -i s/timeout=10/timeout=600/ /usr/lib/python2.7/dist-packages/kicad-automation/util/ui_automation.py && python -m kicad-automation.pcbnew_automation.run_drc /kicad-project/ferris.kicad_pcb "$(pwd)"/build')

DRC_OUTPUT=$(echo $FULL_DRC_OUTPUT | grep "INFO:root" | sed "s/INFO:root//")

if [[ -z "$DRC_OUTPUT" ]]; then
	echo -e "\e[1;32mERROR\e[0m"
	echo "Missing DRC report line. Something went wrong"
	echo "$FULL_DRC_OUTPUT"
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
