import os
import sys
import time
import wave

import pyaudio
import simplecoremidi

simplecoremidi.send_midi((0x90, 0x3c, 0x40))
time.sleep(1)
simplecoremidi.send_midi((0x80, 0x3c, 0x40))

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1 if sys.platform == 'darwin' else 2
RATE = 44100
RECORD_SECONDS = 3
MIDI_MIN = 21 # Lowest key on a piano
MIDI_MAX = 108 # Highest key on a piano

p = pyaudio.PyAudio()
device_count = p.get_device_count()
print("Devices: ")
for i in range(device_count):
    print("  ", i, p.get_device_info_by_index(i)["name"])
device_index=int(input(f"Which device would you like to record from (enter a number 0-{device_count-1})? "))

# Conventions for instrument names and Pianoteq:
# "piano" is NY Steinway D Classical
instrument = input("Instrument: ")
edo = input("EDO: ")
directory = f"static/wav/{instrument}/{edo}edo/"
os.makedirs(directory, exist_ok=True)

for midi_number in range(MIDI_MIN, MIDI_MAX + 1):
    with wave.open(os.path.join(directory, f"{midi_number}.wav"), 'wb') as wf:
        p = pyaudio.PyAudio()

        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)

        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, input_device_index=device_index)

        simplecoremidi.send_midi((0x90, midi_number, 0x40))
        print('Recording...')
        for _ in range(0, RATE // CHUNK * RECORD_SECONDS):
            wf.writeframes(stream.read(CHUNK, exception_on_overflow=False))
        print('Done')
        simplecoremidi.send_midi((0x80, midi_number, 0x40))

        stream.close()
        p.terminate()
