#!/usr/bin/env python
from pygame import *
from threading import Thread
import pygame, time, numpy, pygame.sndarray

TEN_C = 523
TEN_CS = 554
TEN_D = 587
TEN_E = 659
TEN_F = 698
TEN_G = 784
TEN_GS = 830
TEN_A = 880
TEN_B = 987
SOP_C = TEN_C * 2
SOP_D = TEN_D * 2
SOP_E = TEN_E * 2
BAS_A = int(TEN_A/2)
REST = 28000
sample_rate = 44100


def play_for(sample_array, ms, volLeft, volRight):
    sound = pygame.sndarray.make_sound(sample_array)
    beg = time.time()
    channel = sound.play(-1)
    channel.set_volume(volLeft,volRight)
    pygame.time.delay(ms)
    sound.stop()
    end = time.time()
    return beg, end
    

def sine_array_onecycle(hz, peak):
    length = sample_rate / float(hz)
    omega = numpy.pi * 2 / length
    xvalues = numpy.arange(int(length)) * omega
    return (peak * numpy.sin(xvalues))
    

def sine_array(hz, peak, n_samples=sample_rate):
    return numpy.resize(sine_array_onecycle(hz, peak), (n_samples,))
    

def play(note, dur):
    f = sine_array(note, 1)
    f = numpy.array(zip (f , f))
    play_for(f , int(dur * 100), 0.5, 0.5)


def play_chord(notes, dur):
    threads = [Thread(target=play, args=(note, dur)) for note in notes]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


def main():
    pygame.mixer.pre_init(sample_rate, -16, 2) # 44.1kHz, 16-bit signed, stereo
    pygame.init()
    # (NOTE, DURATION, GAP)
    black_dog = [
            (REST, 1.5, 0), (TEN_E, 0.5, 0), (TEN_G, 0.5, 0), (TEN_GS, 0.5, 0), (TEN_A, 0.5, 0),  (TEN_E, 0.5, 0),
            (SOP_C, 1, 0), (TEN_B, 1, 0), (SOP_D, 0.5, 0), (SOP_E, 0.5, 0), (SOP_C, .333, 0), (SOP_D, 0.333, 0), (SOP_C, .333, 0),
            (TEN_B, 0.5, 0), (TEN_B, 0.5, 0), (SOP_C, 1, 0), (TEN_B, 1, 0), (TEN_E, 0.5, 1), (TEN_B, 0.5, 1),
            (TEN_B, 0.5, 0), (TEN_E, 0.5, 0), (TEN_A, 0.5, 0), (TEN_D, 0.5, 0), (TEN_E, 0.5, 0), ((TEN_E, BAS_A, TEN_CS), 1.5, 0)]
    
    for i in range(3):
        for note, dur, pause in black_dog:
            if type(note) == type(()):
                play_chord(note, dur)
            else:
                play(note, dur)


if __name__ == '__main__': 
    main()
