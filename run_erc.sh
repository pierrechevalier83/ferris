ERC_OUTPUT=$(docker run --rm -t -v "$(pwd)"/$1:/kicad-project productize/kicad-automation-scripts python -m kicad-automation.eeschema.schematic run_erc /kicad-project/ferris.sch "$(pwd)"/build | grep "DEBUG:root:Last line" | sed "s/DEBUG:root:Last line:  //")

if [[ -z "$ERC_OUTPUT" ]]; then
	echo -e "\e[1;32mERROR\e[0m"
	echo "Missing ERC report line. Something went wrong"
	exit 2
else
	if [[ "$ERC_OUTPUT" = *"ERC messages: 0  Errors 0  Warnings 0"* ]]; then
		echo -e "\e[1;32mPASS\e[0m"
		echo "$ERC_OUTPUT"
	    exit 0
	else
		echo -e "\e[1;32mFAIL\e[0m"
		echo "$ERC_OUTPUT"
		exit 1
	fi
fi
