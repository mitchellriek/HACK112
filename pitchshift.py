import numpy as np
from pydub import *

def pitchShift(array, shiftFactor):
    # takes an array and shifts the pitch up or down one octave
    newArray = []
    if shiftFactor == 1:
        for i in range(len(array)):
            if i % 2 == 0: newArray = newArray + [array[i]]
    else:
        for i in range(len(array)):
            newArray = newArray + 2*[array[i]]
    return newArray
            

print(pitchShift([2,1,0,1,2,1,0,1,2,1,0,1], -1))
print(pitchShift([2,1,0,1,2,1,0,1,2,1,0,1], 1))

def recursiveEcho(track, deltaVolume = 0, delayLength=200):
    if volume <= -10:
        return track
    else:
        silence = AudioSegment.silent(duration=delayLength)
        currentTrack = silence + track
        return (currentTrack.overlay(recursiveEcho(track, deltaVolume - 2, delayLength)))