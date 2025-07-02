#!/bin/bash

# Path to the user-provided Python script
SCRIPT_PATH="$1"

# Run inside nsjail
nsjail --config nsjail.cfg -- /usr/bin/python3 "$SCRIPT_PATH"
