import sys
import numpy as np
import detect
import matplotlib.pyplot as plt

import pyaudio

CHUNK = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1 if sys.platform == 'darwin' else 2
RATE = 44100
RECORD_SECONDS = 5

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True)

time_series = bytearray()
print('Recording...')
pitches = []
for _ in range(0, RATE // CHUNK * RECORD_SECONDS):
    pitch = detect.find_pitch(np.frombuffer(stream.read(CHUNK), dtype=np.int16))
    pitches += [pitch]
    print(pitch)


print('Done')

plt.plot(np.arange(len(pitches)), pitches)
plt.show()

stream.close()
p.terminate()

