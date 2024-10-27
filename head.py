import librosa
import soundfile as sf
import sounddevice as sd
import numpy as np


eps = 1e-8


def distance(p0, p1):
    return ((p0[0] - p1[0]) ** 2 + (p0[1] - p1[1]) ** 2) ** 0.5


def time_delay(dl, dr):
    return (dl - dr) / 340


def sample_delay(t, r):
    return int(r * t)


def amp_weaken(dl, dr):
    return dl / dr


def watt_weaken(dl, dr):
    return amp_weaken(dl, dr) ** 2


def image(audio, p0, head_size, r):
    dl = distance(p0, (-0.5 * head_size, 0)) + eps
    dr = distance(p0, (0.5 * head_size, 0)) + eps
    delay = sample_delay(time_delay(dl, dr), r)
    weaken = amp_weaken(dl, dr)
    print(dl, dr, delay, weaken)
    if delay > 0:
        al = np.pad(audio, (delay, 0), mode="constant")[:-delay]
        ar = audio
    elif delay < 0:
        al = audio
        ar = np.pad(audio, (-delay, 0), mode="constant")[:delay]
    else:
        al = ar = audio

    if weaken > 1:
        al = al / weaken
    elif weaken < 1:
        ar = ar * weaken

    return np.column_stack((al, ar))


A = (1, 1)
"""
        ^
        |
        |  A
        | /
        |/
--------o-------->
        |
        |
        |
        |
"""

head_size = 0.14 # 自己量量你头多大，两耳距离，米
audio, r = librosa.load("0_1.wav")
naudio = image(audio, A, head_size, r)
sf.write(
    "0_2.wav",
    naudio,
    r,
)

sd.play(naudio, r, blocking=True)

