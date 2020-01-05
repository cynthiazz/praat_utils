import os
import io

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

""" 
Outputs a .txt file where each row contains
audio_file_name	target_word_start_timestamp target_word_end_timestamp (separated by tabs)
for each audio file in the diirectory,
which can be used for further Praat processing.

"""

# set the directory here
directory_str = "/Users/cynthiazhong/Google_Drive/Shen_1920LRAP/DATA/8/"

# loop through each .wav file in directory
directory = os.fsencode(directory_str)
for file in os.listdir(directory):
     filename = os.fsdecode(file)
     # if this is a .wav file, call recognition
     if filename.endswith(".wav"):


# modified from Google speech-to-text API docs
def get_words_and_timestamps(audio_file):
    """Transcribe the given audio file synchronously and output the word time
    offsets."""
    client = speech.SpeechClient()

    with io.open(audio_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
        enable_word_time_offsets=True)

    print("calling recognize...")
    response = client.recognize(config, audio)

    # first result is the most likely
    top_res = response.results[0]

    # get the full transcription 
    alternative = top_res.alternatives[0]
    transc = alternative.transcript
    print(u'Transcript: {}'.format(transc))

    timestamps = {}

    for word_info in alternative.words:
        word = word_info.word
        start_time = word_info.start_time
        end_time = word_info.end_time
        
