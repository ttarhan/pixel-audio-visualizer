#!/bin/bash

set -o xtrace

amixer -d -c 1 cset "numid=9,iface=MIXER,name='Auto Gain Control'" 0
amixer -d -c 1 cset "numid=8,iface=MIXER,name='Mic Capture Volume'" $CAPTURE_GAIN

# nice -n -5 pdm run python main.py
 chrt -f 1 pdm run python main.py