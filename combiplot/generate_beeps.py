#!/usr/bin/env python3
# based on : www.daniweb.com/code/snippet263775.html
import math
import wave
import struct
import csv

# Audio will contain a long list of samples (i.e. floating point numbers describing the
# waveform).  If you were working with a very long sound you'd want to stream this to
# disk instead of buffering it all in memory list this.  But most sounds will fit in 
# memory.
audio = []
sample_rate = 44100.0

#csv_file = "framelog.csv"
#csv_file = "nyorks_log_1.csv"
csv_file = "newout.csv"

debug=True
fps=24.0
data_column = 4 #4 for deaths, 3 for cases
beep_step = 100
a_freq=880
ofn = "badtimes.wav"

#Parse a CSV file and read data lines into list
def read_file(filename, delim=','):
    data = []
    if(debug): print ("Opening file %s" % (filename))
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=delim)
        for row in csv_reader:
          data.append(row)
    if(debug): print(f'Processed {len(data)} lines.')
    return (data)


def append_silence(duration_milliseconds=500):
    """
    Adding silence is easy - we add zeros to the end of our array
    """
    num_samples = duration_milliseconds * (sample_rate / 1000.0)

    for x in range(int(num_samples)): 
        audio.append(0.0)

    return


def append_sinewave(
        freq=440.0, 
        duration_milliseconds=500, 
        volume=1.0):
    """
    The sine wave generated here is the standard beep.  If you want something
    more aggresive you could try a square or saw tooth waveform.   Though there
    are some rather complicated issues with making high quality square and
    sawtooth waves... which we won't address here :) 
    """ 

    global audio # using global variables isn't cool.

    num_samples = duration_milliseconds * (sample_rate / 1000.0)

    for x in range(int(num_samples)):
        audio.append(volume * math.sin(2 * math.pi * freq * ( x / sample_rate )))

    return


def save_wav(file_name):
    # Open up a wav file
    wav_file=wave.open(file_name,"w")

    # wav params
    nchannels = 1

    sampwidth = 2

    # 44100 is the industry standard sample rate - CD quality.  If you need to
    # save on file size you can adjust it downwards. The stanard for low quality
    # is 8000 or 8kHz.
    nframes = len(audio)
    comptype = "NONE"
    compname = "not compressed"
    wav_file.setparams((nchannels, sampwidth, sample_rate, nframes, comptype, compname))

    # WAV files here are using short, 16 bit, signed integers for the 
    # sample size.  So we multiply the floating point data we have by 32767, the
    # maximum value for a short integer.  NOTE: It is theortically possible to
    # use the floating point -1.0 to 1.0 data directly in a WAV file but not
    # obvious how to do that using the wave module in python.
    for sample in audio:
        wav_file.writeframes(struct.pack('h', int( sample * 32767.0 )))

    wav_file.close()

    return

csv_data=read_file(csv_file)
deaths=[int(en[data_column]) for en in csv_data]
minimum_time_gap = 1000
previous_beep_time = 0
frame_time=1.0/ fps
running_time = 0.0
next_beep = beep_step
beep_array = []
prev_count = 0
for i,d in enumerate(deaths):
    running_time += frame_time
    if d>next_beep:
        #Calculate how far through frame...
        deaths_in_frame = d - prev_count
        deaths_after_beep = d - next_beep
        next_beep += beep_step
        if(deaths_in_frame > 0):
            excess_time = (float(deaths_after_beep) / deaths_in_frame) * frame_time
            beep_time = running_time - excess_time
            beep_array.append(beep_time)
            if (beep_time - previous_beep_time) < minimum_time_gap:
                minimum_time_gap = beep_time - previous_beep_time
        previous_beep_time = beep_time
    prev_count=d
on_time_length = 0.7 * minimum_time_gap
if on_time_length < 0.03: on_time_length = 0.03
run_time = 0
for beep in beep_array:
    silence_time = beep - run_time
    if silence_time < 0.003: silence_time = 0.003
    append_silence(duration_milliseconds=(silence_time * 1000.0))
    append_sinewave(freq=a_freq,duration_milliseconds=(on_time_length * 1000.0),volume=0.5)
    run_time = beep + on_time_length
    
#append_sinewave(volume=0.25)
#append_silence()
#append_sinewave(volume=0.5)
#append_silence()
#append_sinewave()
save_wav(ofn)