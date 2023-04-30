# -*- coding: utf-8 -*-
from gtts import gTTS
import pygame.mixer
import pygame.time
import re
import numpy as np
import pysine

import pyaudio


volume = 1.0  # range [0.0, 1.0]
fs = 80000  # sampling rate, Hz, must be integer
duration = 30.0  # in seconds, may be float
lang = "pl"
audio_file = "test.mp3"
lastfreq = 0.0

# 單位Hz, 不是MHz
freqs = ["14-50", "30", "33", "50–90", "83", "136.1", "144.0", "221.23", "230", "288", "426", "440",
         "432", "448.0", "500", "576", "720", "777", "852", "852–936", "888", "936", "963", "2678", "852"]
# freqs = ["1-3000"]

logfile = "./log.txt"


def play_test_frequency2(freq):
    p = pyaudio.PyAudio()
    samples = (np.sin(2 * np.pi * np.arange(fs * duration) * freq / fs)
               ).astype(np.float32)
    output_bytes = (volume * samples).tobytes()
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=fs, output=True)
    stream.write(output_bytes)
    stream.stop_stream()
    stream.close()
    p.terminate()


def play_test_speech(freq):
    mytext = "Numerosi on {} ja lopeta työsi ja sano, että numeroni on {}".format(
        freq, freq, freq, freq)
    audio = gTTS(text=mytext, lang=lang, slow=False)
    audio.save(audio_file)
    pygame.mixer.init()
    tada = pygame.mixer.Sound(audio_file)
    channel = tada.play()
    while channel.get_busy():
        pygame.time.wait(100)  # ms

    f = open(logfile, "a")
    f.write("{}\n".format(freq,))
    f.close()


def play_test_frequency(freq):
    pysine.sine(frequency=freq, duration=duration)


for x in freqs:
    if re.findall(r'^([0-9\.]*)-([0-9\.]*)$', x, re.IGNORECASE | re.S | re.U):
        m = re.findall(r'^([0-9\.]*)-([0-9\.]*)', x,
                       re.IGNORECASE | re.S | re.U)
        startf = m[0][0]
        endf = m[0][1]
        mylist = list(range(int(startf), int(endf)))
        for y in mylist:
            for i in range(0, 10):
                freq = "{}.{}".format(y, i)
                freq = float(freq)
                if freq < lastfreq:
                    continue
                print("play frequency {}".format(freq))
                play_test_frequency2(freq)
                play_test_speech(freq)
    elif re.findall(r'^([0-9\.]*$)', x, re.IGNORECASE | re.S | re.U):
        if x.isdigit():
            for i in range(0, 10):
                freq = "{}.{}".format(x, i)
                freq = float(freq)
                if freq < lastfreq:
                    continue
                print("play frequency {}".format(freq))
                play_test_frequency2(freq)
                play_test_speech(freq)
        else:
            freq = float(freq)
            if freq < lastfreq:
                continue
            print("play frequency {}".format(freq))
            play_test_frequency2(freq)
            play_test_speech(freq)
