amixer -d -c 2 cset "numid=9,iface=MIXER,name='Auto Gain Control'" 0
amixer -d -c 2 cset "numid=8,iface=MIXER,name='Mic Capture Volume'" 5
PA_MIN_LATENCY_MSEC=4 python main.py