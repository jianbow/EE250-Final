# GITHUB REPO: https://github.com/usc-ee250-fall2020/lab08-lab08
# GROUP MEMBERS: Leo Zhuang and Richard Huang

import numpy as np
from pydub import AudioSegment
import os
import sys

SLICE_SIZE = 0.1 #seconds
WINDOW_SIZE = 0.2 #seconds
NUMBER_DIC = {}


def get_max_frq(frq, fft):
    max_frq = 0
    max_fft = 0
    for idx in range(len(fft)):
        if abs(fft[idx]) > max_fft:
            max_fft = abs(fft[idx])
            max_frq = frq[idx]
    return max_frq

def main(file):
    print("Importing {}".format(file))
    audioFull = AudioSegment.from_mp3(file)
    audio = audioFull[0:10000]
    sample_count = audio.frame_count()
    sample_rate = audio.frame_rate
    samples = audio.get_array_of_samples()

    period = 1/sample_rate                     #the period of each sample
    duration = sample_count/sample_rate         #length of full audio in seconds

    slice_sample_size = int(SLICE_SIZE*sample_rate)   #get the number of elements expected for [SLICE_SIZE] seconds
    n = slice_sample_size                            #n is the number of elements in the slice

    #generating the frequency spectrum
    k = np.arange(n)                                #k is an array from 0 to [n] with a step of 1
    slice_duration = n/sample_rate                   #slice_duration is the length of time the sample slice is (seconds)
    frq = k/slice_duration                          #generate the frequencies by dividing every element of k by slice_duration

    #max_frq_idx = int(MAX_FRQ*slice_duration)       #get the index of the maximum frequency (2000)
    frq = frq[range(2000)]                   #truncate the frequency array so it goes from 0 to 2000 Hz

    start_index = 0                                 #set the starting index at 0
    end_index = start_index + slice_sample_size      #find the ending index for the slice
    output = ''

    print()
    baby_freq_cnt = 0
    i = 0
    while end_index < len(samples):
        i += 1
        #TODO: grab the sample slice and perform FFT on it
        sample_slice = samples[start_index: end_index]
        sample_slice_fft = np.fft.fft(sample_slice)/n
        #TODO: truncate the FFT to 0 to 2000 Hz
        sample_slice_fft = sample_slice_fft[range(2000)] #truncate the sample slice fft array so it goes from 0 to 2000 Hz
        #TODO: calculate the locations of the upper and lower FFT peak using get_peak_frqs()
        #result = get_peak_frqs(frq,abs(sample_slice_fft))
        result = 2*get_max_frq(frq,abs(sample_slice_fft))
        #TODO: print the values and find the number that corresponds to the numbers
        #print(result)
        if(450 < result < 2000):
            baby_freq_cnt += 1
        #print(get_number_from_frq(result[0],result[1]))
        #Incrementing the start and end window for FFT analysis
        start_index += int(WINDOW_SIZE*sample_rate)
        end_index = start_index + slice_sample_size

    #print("Program completed")
    #print("User typed: " + str(output))
    #print(baby_freq_cnt)
    #print(i)
    if(baby_freq_cnt >= .5*i):
        print("baby crying")
        #print(baby_freq_cnt/i)
        return True
    else:
        print("not baby")
        return False

if __name__ == '__main__':
    if len(sys.argv) != 2 or not os.path.isfile(sys.argv[1]):
        print("Usage: baby_freq.py [file]")
        exit(1)
    main(sys.argv[1])
