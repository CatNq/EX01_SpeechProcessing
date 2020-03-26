import librosa
import soundfile as sf
import sounddevice as sd
import numpy as np
import queue
import sys
import threading

FILE_APPEND = "sentences"
OUTPUT_DIR = "./output"

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

print("\n")
print("Extracted {} sentences from file.".format(len(file_extracted_content)))
print("Default output prefix is " + FILE_APPEND + "_#.wav\n")
print("\n")

inputQueue = queue.Queue()

def read_kb_input(inputQueue):
    while True:
        input_str = input()
        inputQueue.put(input_str)

#Display text and recording
def mainRecording():
    inputThread = threading.Thread(target=read_kb_input, args=(inputQueue,), daemon=True)
    inputThread.start()
    i = 0
    for s in file_extracted_content:
        print("\"{}.\"\n".format(s))
        file_name = OUTPUT_DIR + "/" + FILE_APPEND + "_{}.wav".format(i)
        i += 1
        print("Output: " + file_name)
        input("Press any key to start recording.\n")
    return

mainRecording()