import sys
import numpy as np
from utils import detect
from utils import interpret
import matplotlib.pyplot as plt
import time

import pyaudio

CHUNK = 512
SAMPLE_SIZE = 4 * CHUNK
FORMAT = pyaudio.paInt16
CHANNELS = 1 if sys.platform == 'darwin' else 2
RATE = 44100
RECORD_SECONDS = 5

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True)

print('Recording...')
pitches = []
sample = np.frombuffer(stream.read(SAMPLE_SIZE), dtype=np.int16)
for _ in range(0, RATE // CHUNK * RECORD_SECONDS):
    pitch = detect.find_pitch(sample)
    pitches += [pitch]

    sample = np.append(sample[CHUNK:SAMPLE_SIZE], np.frombuffer(stream.read(CHUNK), dtype=np.int16))
    # sample[:SAMPLE_SIZE-CHUNK] = sample[CHUNK:SAMPLE_SIZE]
    # sample[SAMPLE_SIZE-CHUNK:] = np.frombuffer(stream.read(CHUNK), dtype=np.int16)

    start_time = time.time()
    interpret.print_note(pitch)


print('Done')

plt.scatter(np.arange(len(pitches)), pitches, marker='.')
plt.show()

stream.close()
p.terminate()

