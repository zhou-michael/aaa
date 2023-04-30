import wave
import pyaudio
import numpy as np

def write_to_wave(array):
    time_series = array.tobytes()
    with wave.open("test.wav", 'wb') as wf:
        data = array.tobytes()
        wf.setnchannels(1)
        wf.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)

        wf.writeframes(time_series)

with wave.open("output.wav", 'rb') as wf:
    audio = wf.readframes(wf.getnframes())

    time_series = np.frombuffer(audio, dtype=np.int16)

write_to_wave(time_series)

