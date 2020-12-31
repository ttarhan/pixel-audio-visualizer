import pyaudio
import struct
import numpy as np
from matplotlib import pyplot as plt
from scipy import signal
from scipy import fftpack as fft
import sacn
import time
#from pyAudioAnalysis import ShortTermFeatures as stf
#import STF

FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 48000
#RATE = 20000
FPS=20
CHUNK = int(RATE/20)
LEDS = 412


running = False
# CHUNK = int(RATE/40)
#WINDOW = round(RATE * 0.010)

# plt.ion()
# plt.show()


def groupbins(bins, data):
    current = []
    curbin = bins[0]

    for (i,d) in enumerate(bins):
        if d != curbin:
            yield current
            current = []
            curbin = d

        current.append(data[i])
    
    yield current



sender = sacn.sACNsender(fps=40)
sender.start()

sender.activate_output(5)
sender[5].multicast = True

sender.activate_output(6)
sender[6].multicast = True

sender.activate_output(7)
sender[7].multicast = True

run = True

audio = pyaudio.PyAudio()

stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)


#for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):

frequencies = fft.rfftfreq(CHUNK, 1/RATE)
print("Axis")
print(frequencies)

# np.set_printoptions(threshold=500000)

bins = np.linspace(50, 4500, LEDS)
binned = np.digitize(frequencies, bins)

# Digitize returns a bin after our last bin for out-of-range items; chop it off
binned = binned[binned < LEDS] 

print("Bins")
print(bins)

print("Binned")
print(binned)

# plt.ylim([0, 40])
# plt.xlim([50, 4500])

ln = None

lt = time.time()

while run:
    data = stream.read(CHUNK, exception_on_overflow=False)
    data = np.frombuffer(data, dtype=np.float32)
    result = abs(fft.rfft(data))
    dBS = 10 * np.log10(result)

    #histogram = np.histogram()

    # x = np.empty(150)
    # x[binned] = result[binned]

    # values = [[] for (x) in range(0,151)]
    
    # for (i,v) in enumerate(abs(result)):
    #     values[binned[i]].append(v)

    # print("Values")
    # print(values)

    newvalues = list(groupbins(binned, result))

    # print("New")
    # print(newvalues)

    maxvalues = [max(m) if len(m) else 0 for m in newvalues]

    # print("Max")
    # print(len(maxvalues))

    dmxData = np.full(LEDS*3, 0, dtype=np.uint8)

    # for (i,v) in enumerate(newvalues):
    #     if len(v) == 0 or max(v) < 10:
    #         continue
        
    #     dmxData[i*3:i*3+3] = 255

    for (i,v) in enumerate(maxvalues):
        # print(f'i: {i}, v: {v}')
        if v < 10:
            continue
        
        dmxData[i*3:i*3+3] = 255

    sender[5].dmx_data = dmxData[0:170*3]
    sender[6].dmx_data = dmxData[170*3:340*3]
    sender[7].dmx_data = dmxData[340*3:]

    # print(len(dmxData[0:170*3]))
    # print(len(dmxData[170*3:340*3]))
    # print(len(dmxData[340*3:]))

    if ln is not None:
        ln.remove()

    # ln, = plt.plot(frequencies,result)
    ln, = plt.plot(dmxData)
    plt.pause(0.005)
    print(f'Diff: {round(time.time()-lt,4)}')
    lt = time.time()
    # run = False

sender.stop()

# while run:
#     data = stream.read(CHUNK, exception_on_overflow=False)
#     #data = np.array(struct.unpack(str(2 * CHUNK) + 'B', data), dtype='b')
#     data = np.frombuffer(data, dtype=np.float32)
#     f, t, Sxx = signal.spectrogram(data, fs=RATE)
#     dBS = 10 * np.log10(Sxx)
#     plt.pcolormesh(t, f, dBS)
#     #plt.colorbar()
#     plt.pause(0.005)

# print("Axis")
# print(len(np.fft.fftfreq(CHUNK, 1/RATE)))


# print("Data")
# while (run):
#     data = stream.read(CHUNK)
#     frame = np.frombuffer(data, dtype=np.float32)
#     fft = np.fft.fft(frame)
#     print(len(fft))
#     print(fft)
#     run=False



# while (run):
#     data = stream.read(CHUNK)
#     frame = np.frombuffer(data, dtype=np.float32)
#     specgram, time_axis, freq_axis = STF.spectrogram(frame, sampling_rate=RATE, window=WINDOW, step=WINDOW, plot=True)
#     print("Time")
#     print(time_axis)
#     print("Frequency")
#     print(freq_axis)
#     print("Values")
#     print(specgram)
#     run = False
#     # print(frame.max())
#     # plt.cla()
#     # plt.ylim([-1, 1])
#     # plt.plot(frame)
#     # plt.draw()
#     # plt.pause(0.000000000001)

stream.stop_stream()
stream.close()
audio.terminate()

