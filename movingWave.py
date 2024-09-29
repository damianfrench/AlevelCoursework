
import numpy as np
import webrtcvad
import sounddevice as sd
from scipy.io.wavfile import write,read
from scipy.fft import fft, hfft2
import librosa
from librosa import display
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import WorkingOutWords
import sqlite3
global count
count=0
def main(pause,ear):
    vad=webrtcvad.Vad()
    vad.set_mode(0)
    file_path="output.wav"
    data=read(file_path) #loads audio file and stores the aplitudes and sample rate
    sampling_rate=data[0]
    samples=data[1]
    #duration=len(samples)/sampling_rate
    # plt.figure() # creates a figure to draw our graph on 
    # plt.plot(samples) #creates the graph of original audio
    # plt.xlabel("Time (Seconds) -->")
    # plt.ylabel("Amplitude")
    # plt.savefig("audio.png")
    # plt.show()
    # plt.close()
    phoneme_time=0.2 #constant - set max amount of time that one phoneme can take up.
    phonem_overlap=0.5 # constant - overlapping amount so that each phoneme can be up to 50% into the previous or next window
    #3/0.2=15
    #48000/150=320 = num of samples in window
    #150 is the num of windows in recording
    windows_in_recording=int((len(samples)/sampling_rate)/phoneme_time) # calculates how many windows in the current recording
    samples_in_window=int(len(samples)/windows_in_recording) # calculates how many samples there are per window
    stride_value=int(samples_in_window*phonem_overlap) # calcualtes how many samples into the previous and next windows we look for our phoneme in

    #going 50% into the next window by 160
    words=[]
    for p in range(windows_in_recording+1): # loops through all the windows in the recording
        if p==0: # error case as we cannot go into the previous window
            words.append(fft_plot(samples[0:((p+1)*samples_in_window)+stride_value],sampling_rate,p,pause,ear))
            continue
        elif p==windows_in_recording+1: # error case as we cannot go into the next window
            words.append(fft_plot(samples[(p*samples_in_window)-stride_value:p*(samples_in_window)],sampling_rate,p,pause,ear))
            continue
        words.append(fft_plot(samples[(p*samples_in_window)-stride_value:((p+1)*samples_in_window)+stride_value],sampling_rate,p,pause,ear)) #performs a fourier transform on the given window, 
        continue
    return words
        #extended by 50% into the previous and next windows



def fft_plot(audio,sampling_rate,p,pause,ear):
    n=len(audio)
    y=fft(audio)
    frequencies=np.linspace(0,sampling_rate/2,n//2) #splits the x axis into n//2 evenly spaced sections starting at 0 and ending at half the sampling rate
    # according to nyquist sampling theorem
    #fig, ax=plt.subplots()
    y_plotting=2.0/n*np.abs(y[:n//2]) # creates an array of the absolute values of the second half of the fourier transform values returned from the fft function
    Hf=highest_freq(y_plotting,frequencies) #produces and array that contains the 10 frequencies with the highest magnitude
    #ax.plot(frequencies,y_plotting) # plots graph of frequency against time
    # plt.grid()
    # plt.xlabel("Frequency -->")
    # plt.ylabel("Magnitude")
    # plt.savefig("frame{}".format(p+1))
    # plt.show()
    #overlappingWaves(Hf)
    print(Hf)
    sumDifference={}
    if pause==True:
        #if we have recorded the pause sound
        WorkingOutWords.Pause(Hf)
    elif ear==True:
        #if we have recorded the "ear" sound 
         WorkingOutWords.ear(Hf)
    # WorkingOutWords.adding(Hf)
        #array storing sum of percentage difference
    else:
        for x in range(len(Hf)):
            #loops through Hf 
            freqs=WorkingOutWords.Database(x+1)
                    #outputs the frequencies from all the phonemes in english
            closeness=WorkingOutWords.Comparing(Hf[x],freqs)
                    #returns an array of how close our freqs are to each phoneme
            for p in closeness:
                if p[-1] not in sumDifference.keys():
                    sumDifference[p[-1]]=p[0]
                else:
                    sumDifference[p[-1]]+=p[0]
                #loops through closeness and adds the value of the percentage difference to the dict sumDifference
        print(sumDifference)
        return min(sumDifference,key=sumDifference.get)





def highest_freq(y_plotting,x):
    ind=np.sort(y_plotting)[::-1] # creates an sorted version of the y_plotting array
    Highest_frequencies=[] 
    for m in range(len(ind[:10])): # loops through the first 10 values in the sorted array, i.e. the highest amplitudes in the window
        Highest_frequencies.append(x[np.where(y_plotting==ind[m])[0][0]]) # finds the index of the current amplitude in y_plotting, 
        #and then finds the value of x at this index,
        # which will give us the frequency at that amplitude
    return Highest_frequencies

def overlappingWaves(Hf):
    sr=16
    ts=1.0/sr
    t=np.arange(0,1,ts)
    plt.title("Frequencies")
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    for x in range(len(Hf)):
        y=np.sin(2*np.pi*Hf[x]*t)
        plt.plot(t,y)
    plt.show()
