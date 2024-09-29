from audioop import rms
import pyaudio
import struct
import math
import time
import wave
import librosa
from librosa import display
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import movingWave
import sqlite3


FORMAT=pyaudio.paInt16
CHANNELS=1
RATE=16000
chunk=1024
SHORT_NORMALIZE=(1.0/327680)
TIMEOUT=2



class Recorder:
    global threshold
    global recorded
    global words
    global daya

    def rms(self,frame):
        count = len(frame) / 2
        format = "%dh" % (count)
        shorts = struct.unpack(format, frame)

        sum_squares = 0.0
        for sample in shorts:
            n = sample * SHORT_NORMALIZE
            sum_squares += n * n
        rms = math.pow(sum_squares / count, 0.5)
        return rms * 1000
        #returns a value for the power of the sound

    def __init__(self):
        global threshold
        threshold = 5
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  input=True,
                                  output=True,
                                  frames_per_buffer=chunk)
                                  #initiates the recorder

    def listening(self):
        global words
        words=[]
        now=time.time()
        print("listening...",end="")
        rmsBaseline=0
        while True:
            input=self.stream.read(chunk,exception_on_overflow=False)
            if rmsBaseline==0:
                rmsBaseline=self.rms(input)
                time.sleep(1)
            rmsValue=self.rms(input)
            print(rmsBaseline)
            print(rmsValue)
            if rmsValue> rmsBaseline+threshold:
                self.recording(rmsBaseline+threshold)
                now=time.time()
            else:
                rmsBaseline=0.0
                rmsBaseline=rmsValue
                print(rmsBaseline)
            if time.time()>now+5:
                break
            #print(rmsBaseline)
        print("\nStopping")
        return self.stop()

    # def listening(self):
    #     global words
    #     words=[]
    #     now=time.time()
    #     print("listening...",end="")
    #     rmsBaseline=0.0
    #     while True:
    #         if self.stream.is_active()==False:
    #             return words
    #         for x in range(1,5):
    #             print(x)
    #             time.sleep(1)
    #         self.recording(rmsBaseline+threshold)
    #         break
    #         if time.time()>now+10:
    #             break
    #         #print(rmsBaseline)
    #     print("\nStopping")
        # return words


    def recording(self,Threshold):
        global recorded
        recorded=[]
        now=time.time()
        end=time.time()+TIMEOUT
        print("\nrecording")
        while now<=end:
            data=self.stream.read(chunk,exception_on_overflow=False)
            recorded.append(data)
            if self.rms(data)>=Threshold:
                end=time.time()+TIMEOUT
            now=time.time()
        words.append(self.writing(b''.join(recorded)))
        print(words)
    
    def PauseSound(self):
        #records for 5 seconds and then runs pauseWriting()
        global recorded
        recorded=[]
        now=time.time()
        print("\nrecording")
        while time.time()<=now+5:
            data=self.stream.read(chunk,exception_on_overflow=False)
            recorded.append(data)
        self.pauseWriting(b''.join(recorded))

    def pauseWriting(self,recorded):
        #takes the recording of the background and runs the movingwave.main() function on it.
        fileName= 'output.wav'
        f=wave.open(fileName,'wb')
        f.setnchannels(CHANNELS)
        f.setsampwidth(self.p.get_sample_size(FORMAT))
        f.setframerate(RATE)
        f.writeframes(recorded)
        f.close()
        print("writen to file {}".format(fileName))
        print("listening")
        print("Hello")
        movingWave.main(True,False)#specificies that it is the "space" sound that is being inputted

    def earWriting(self,recorded):
        #takes the recording of the sound "ear" and runs movingwave.main() function on it.
        fileName= 'output.wav'
        f=wave.open(fileName,'wb')
        f.setnchannels(CHANNELS)
        f.setsampwidth(self.p.get_sample_size(FORMAT))
        f.setframerate(RATE)
        f.writeframes(recorded)
        f.close()
        print("writen to file {}".format(fileName))
        print("listening")
        movingWave.main(False,True) #specifies that it is the "ear" sound being inputted
    
    def earSound(self):
        # records for 5 seconds and then runs earWriting()
        global recorded
        recorded=[]
        now=time.time()
        print("\nrecording")
        while time.time()<=now+5:
            data=self.stream.read(chunk,exception_on_overflow=False)
            recorded.append(data)
        self.earWriting(b''.join(recorded))

    def writing(self,recorded):
        fileName= 'output.wav'
        f=wave.open(fileName,'wb')
        f.setnchannels(CHANNELS)
        f.setsampwidth(self.p.get_sample_size(FORMAT))
        f.setframerate(RATE)
        f.writeframes(recorded)
        f.close()
        print("writen to file {}".format(fileName))
        print("listening")
        data=movingWave.main(False,False)
        #self.listening()
        print("ending")
        db=sqlite3.connect("/Users/damianjoshuafrench/Desktop/coursework-1/frequencies.db")
        print(data)
        dataP=[]
        for x in data:
            dataP.append(db.execute("""select Spelling from Phonemes where Phoneme == (?)""",("{}".format(x),)).fetchall()[0][0])
        db.close()
        print(dataP)
        return dataP


        #movingWave.main()
    #    self.plotting()

    # def plotting(self):
    #     fig=plt.figure()
    #     ax1 = fig.add_subplot(1,1,1)
    #     while True:
    #         self.animate()
    #         ani = animation.FuncAnimation(fig, self.animate(), interval=1000)
    #         plt.show()

    # def animate(self):
    #     file_path="output.wav"
    #     samples,sampling_rate=librosa.load(file_path,sr=None,mono=True,offset=0.0,duration=None)
    #     librosa.display.waveshow(y=samples,sr=sampling_rate)

    def stop(self):
        global recorded
        self.stream.stop_stream()    # "Stop Audio Recording
        self.stream.close()          # "Close Audio Recording
        self.p.terminate()
        words.append(self.writing(b''.join(recorded)))
        print("words=","".join(words[0]))
        return "".join(words[0])
    
    def changeThreshold(self, newThreshold):
        #updates the threshold variable with the slider value
        global threshold
        print(newThreshold)
        threshold+=newThreshold
        print(threshold)



#https://stackoverflow.com/questions/20951755/how-to-use-struct-pack-unpack-with-pyaudio-correctly

#https://stackoverflow.com/questions/18406570/python-record-audio-on-detected-sound

#https://github.com/wiseman/py-webrtcvad


# def main():
#     global device
#     device=Recorder()
#     device.listening()



# if __name__=="__main__":
#     main()
#     #movingWave.main()
