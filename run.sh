#!/bin/bash

set -xeuo pipefail

# Detect if running in k8s
if [ -f /var/run/secrets/kubernetes.io/serviceaccount/token ] || [ "$KUBERNETES_SERVICE_HOST" != "" ]; then
	# Only run this block if in k8s
	if [ ! -f /data/config.py ]; then
		cp ./visualizer/config.py /data/config.py
	fi
	cp /data/config.py ./visualizer/config.py

	# Allow environment variables to be set in /data/env
	if [ ! -f /data/env ]; then
		touch /data/env
	fi

    set -a
    . /data/env
    set +a
fi

amixer -d -c 0 cset "numid=9,iface=MIXER,name='Auto Gain Control'" 0
amixer -d -c 0 cset "numid=8,iface=MIXER,name='Mic Capture Volume'" $CAPTURE_GAIN

# nice -n -5 .venv/bin/visualizercli
 chrt -f 1 .venv/bin/visualizercli
