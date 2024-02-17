from typing import Iterable
import time
import numpy as np
import pyaudio


def play_sine_wave(frequencies: Iterable[float], duration: float = 1000, volume: float = .5):
    """
    :param frequencies: Iterable of frequencies, in Hz
    :param duration: duration, in milliseconds
    :param volume: volume, between 0.0 and 1.0
    :return:
    """

    p = pyaudio.PyAudio()

    sampling_rate = 44100  # sampling rate, Hz, must be integer
    frames = round((sampling_rate * duration) / 1000)

    samples = np.zeros(frames)

    for frequency in frequencies:
        # generate samples, note conversion to float32 array
        samples = np.add(samples, np.sin(2 * np.pi * np.arange(frames) * frequency / sampling_rate)).astype(np.float32)

    # per @yahweh comment explicitly convert to bytes sequence
    output_bytes = (volume * samples).tobytes()

    # for paFloat32 sample values must be in range [-1.0, 1.0]
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=sampling_rate,
                    output=True)

    # play. May repeat with different volume values (if done interactively)
    start_time = time.time()
    stream.write(output_bytes)
    print("Played sound for {:.2f} seconds".format(time.time() - start_time))

    stream.stop_stream()
    stream.close()

    p.terminate()