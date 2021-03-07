#!/bin/bash
if [[ -z "$WORKDIR" ]]; then
	export WORKDIR="$(pwd)";
fi

docker run -e WORKDIR=$WORKDIR -v $WORKDIR:/workdir -v /var/run/docker.sock:/var/run/docker.sock -t pierrechevalier83/ferris_automation ninja $@

