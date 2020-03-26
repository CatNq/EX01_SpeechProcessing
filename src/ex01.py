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
text_file = open('speech.txt', 'r')
text_content = text_file.readlines()

#Format the sentences
text_extracted_content = []

#Remove and cut blank spaces between each sentences
for sc in text_content:
    sentences = sc.split('.')
    for s in sentences:
        text_extracted_content.append(s.strip())
text_extracted_content = [s for s in text_extracted_content if s]

print("Extracted {} sentences from file.".format(len(text_extracted_content)))

print("Default output prefix is " + FILE_APPEND + "_#.wav")

print("Outputting to " + OUTPUT_DIR + "/" + FILE_APPEND + "_#.wav\n")
