#!/bin/bash

if [[ -z "${MDPMC_DIR}" ]]; then
	export MDPMC_DIR="$( realpath $( dirname "${BASH_SOURCE[0]}" ) )"
	echo "MCPMC_DIR=$MDPMC_DIR"
fi
