amixer -d -c 3 cset "numid=9,iface=MIXER,name='Auto Gain Control'" 0
amixer -d -c 3 cset "numid=8,iface=MIXER,name='Mic Capture Volume'" 28
#PA_MIN_LATENCY_MSEC=4 pdm run python main.py

pdm run python main.py
