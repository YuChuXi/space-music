import librosa
import soundfile
import numpy as np


eps = 1e-5


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

def image(audio, p0, head_size, r):
    dl = distance(p0, (0.5*head_size, 0)) + eps
    dr = distance(p0, (0.5*head_size, 0)) + eps
    delay = sample_delay(delay(dl, dr), r)
    weaken = amp_weaken(dl, dr)
    if delay >0:
        al = np.pad(audio, (delay, 0), mode="constant")[:delay]
        ar = audio
    elif delay < 0:
        al = audio
        ar = np.pad(audio, (-delay, 0), mode="constant")[:-delay]
    else:
        al = ar = audio

    if weaken >1:
        ar = ar / weaken
    elif weaken < 1:
        al = al * weaken
    
    return np.column_stack((al, ar))



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

head_size = 0.35
audio, r = librosa.load("0_1.wav")
naudio = image(audio, A, head_size, r)
print(naudio)
soundfile.write("0_2.wav", naudio, r, )