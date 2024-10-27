import librosa
import numpy


head_zize = 0.35
eps = 1e-5

A = (1, 2)

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


def distance(p0, p1):
    return ((p0[0] - p1[0]) ** 2 + (p0[1] - p1[1]) ** 2) ** 0.5

def delay(dl, dr):
    return (dl - dr) / 340

def sample_delay(t, r):
    return r * t

def amp_weaken(dl, dr):
    return dl / dr

def watt_weaken(dl, dr):
    return amp_weaken(dl, dr)**2

def image(audio, p0, head_size):
    dl = distance(p0, (0.5*head_size, 0)) + eps
    dr = distance(p0, (0.5*head_size, 0)) + eps
    delay = sample_delay(delay(dl, dr))
    weaken = amp_weaken(dl, dr)

    return audio


audio = librosa.load("0_1.wav")
print(image(audio))