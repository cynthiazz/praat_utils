import os

# TEST 1: run Praat script (boundary-selector) via Python
# import subprocess
# directory = "/Users/cynthiazhong/Google_Drive/Shen_1920LRAP/DATA/8/"
# filename = "8_39_en_n.wav"
# start = "2.0"
# end = "2.2"

# subprocess.call(['/Applications/Praat.app/Contents/MacOS/Praat', '--run', 'boundary-selector.praat', directory, filename, start, end])

# rip praat doesn't allow view/edit script commands when running from command line

# TEST 2: loop through stuff in a directory
directory_str = "/Users/cynthiazhong/Google_Drive/Shen_1920LRAP/DATA/8/"

directory = os.fsencode(directory_str)
for file in os.listdir(directory):
     filename = os.fsdecode(file)
     # if this is a .wav file, call recognition
     if filename.endswith(".wav"):
     	print(filename)

# Imports the Google Cloud client library
# from google.cloud import speech
# from google.cloud.speech import enums
# from google.cloud.speech import types