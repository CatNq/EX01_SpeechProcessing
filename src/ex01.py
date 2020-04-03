import librosa
import soundfile as sf
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import queue
import sys
import threading
import speech_recognition as sr

FILE_APPEND = "sentences"
OUTPUT_DIR = "./output"
SAMPLE_RATE = 44100
MAXIMUM_DURATION = 3600
CHANNELS = 2

#Read files
file = open('speech.txt', 'r')
file_content = file.readlines()

#Format the sentences
file_extracted_content = []

#Remove and cut blank spaces between each sentences
for sc in file_content:
    sentences = sc.split('.')
    for s in sentences:
        file_extracted_content.append(s.strip())
file_extracted_content = [s for s in file_extracted_content if s]

print("Extracted {} sentences from file.".format(len(file_extracted_content)))
print("Default output prefix is " + FILE_APPEND + "_#.wav\n")
print("___________________________")
print("\n")

inputQueue = queue.Queue()

def read_kb_input(inputQueue):
    while True:
        input_str = input()
        inputQueue.put(input_str)

new_append = input("Input: ")
if (new_append):
    FILE_APPEND = new_append
 
print("Outputting to " + OUTPUT_DIR + "/" + FILE_APPEND + "_#.wav\n")

print("Program will now record the sentences.\n")


inputQueue = queue.Queue()

def read_kb_input(inputQueue):
    while True:
        input_str = input()
        inputQueue.put(input_str)


q = queue.Queue()

def callback( indata, frames, time, status):
    #This is called (from a separate thread) for each audio block.
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())

def record(file_name):

    try:
        #Open a new soundfile and attempt recording
        with sf.SoundFile(file_name, mode='x', samplerate=SAMPLE_RATE, channels=CHANNELS, subtype="PCM_24") as file:
            with sd.InputStream(samplerate=SAMPLE_RATE, device=sd.default.device, channels=CHANNELS, callback=callback):
                print("Recording ... Press any key to stop")
                
                while True:
                    file.write(q.get())

                    if (inputQueue.qsize() > 0):
                        input_str = inputQueue.get()
                        if (KeyboardInterrupt):
                            break
                print("Saved to: {}\n".format(file_name))

    except Exception as e:
        print(e)



#Recording
def mainRecording():
    inputThread = threading.Thread(target=read_kb_input, args=(inputQueue,), daemon=True)
    inputThread.start()

    i = 0
    for s in file_extracted_content:
        print("\"{}.\"\n".format(s))
        file_name = OUTPUT_DIR + "/" + FILE_APPEND + "_{}.wav".format(i)
        i += 1
        print("Output: " + file_name)
        input("Press any key to start recording.")
        record(file_name)
    return

mainRecording()