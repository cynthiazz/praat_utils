import os
import io

# TEST 1: run Praat script (boundary-selector) via Python
# import subprocess
# directory = "/Users/cynthiazhong/Google_Drive/Shen_1920LRAP/DATA/8/"
# filename = "8_39_en_n.wav"
# start = "2.0"
# end = "2.2"

# subprocess.call(['/Applications/Praat.app/Contents/MacOS/Praat', '--run', 'boundary-selector.praat', directory, filename, start, end])

# rip praat doesn't allow view/edit script commands when running from command line

# TEST 2: manipulating files in a directory
# directory_str = "/Users/cynthiazhong/Google_Drive/Shen_1920LRAP/DATA/8/"

# directory = os.fsencode(directory_str)
# for file in os.listdir(directory):
#      filename = os.fsdecode(file)
#      # if this is a .wav file, call recognition
#      if filename.endswith(".wav"):
#      	print(filename)

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

from google.cloud import speech_v1

# # TEST 3: getting word timestamps
# def sample_long_running_recognize(file_dir):
#     """
#     Print start and end time of each word spoken in audio file from local directory

#     Args:
#       file_dir: abs path for audio file on local machine
#     """

#     client = speech_v1.SpeechClient()

#     # When enabled, the first result returned by the API will include a list
#     # of words and the start and end time offsets (timestamps) for those words.
#     enable_word_time_offsets = True

#     # The language of the supplied audio
#     language_code = "zh"
#     config = {
#         "enable_word_time_offsets": enable_word_time_offsets,
#         "language_code": language_code,
#     }

#     # Loads the audio into memory
#     with io.open(file_dir, 'rb') as audio_file:
#     	content = audio_file.read()
#     	audio = types.RecognitionAudio(content=content)

#     operation = client.long_running_recognize(config, audio)

#     print(u"Waiting for operation to complete...")
#     response = operation.result()

#     # The first result includes start and end time word offsets
#     result = response.results[0]
#     # First alternative is the most probable result
#     alternative = result.alternatives[0]
#     print(u"Transcript: {}".format(alternative.transcript))
#     # Print the start and end time of each word
#     for word in alternative.words:
#         print(u"Word: {}".format(word.word))
#         print(
#             u"Start time: {} seconds".format(
#                 word.start_time.seconds, word.start_time.nanos
#             )
#         )
#         print(
#             u"End time: {} seconds {} nanos".format(
#                 word.end_time.seconds, word.end_time.nanos
#             )
#         )

# sample_long_running_recognize("./test/8_10_ch_n.wav")

# TEST 4: locate target word in monolingual sentence
test_dir = "./test/"

# target words in monolingual english sentences
target_mono_en = ["bee", "beetle", "mountain", "lamp", "goat", "monkey", 
                "artichoke", "diamond", "leaf", "shark", "tulip", "bus", 
                "coat", "pipe", "cherry", "ball", "phone", "peach", "tie"]

# target words in monolingual chinese sentences
# target_mono_zh = ["苹果", "西瓜", "毛巾", "蓝宝石", "勺子", "杯子", "报纸", 
#                 "面包", "气球", "电视", "心", "礼物", "树", "糖", "袜子",
#                 "手机", "恐龙", "凳子"]
target_mono_zh = ["苹", "西", "毛", "蓝", "勺", "杯", "报", "面", "气", "电", "心", "礼", 
                "树", "糖", "袜", "手", "恐", "凳"]

# modified from Google speech-to-text API docs
def find_taget_boundaries_mono(audio_file_path, lang):
    """ Transcribe the given audio file synchronously and 
    return the time offsets of the target word it contains. """

    client = speech.SpeechClient()

    with io.open(audio_file_path, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code=lang,
        enable_word_time_offsets=True)

    print("calling recognize...")
    response = client.recognize(config, audio)

    # first result is the most likely
    top_res = response.results[0]

    # get the full transcription 
    top_alt = top_res.alternatives[0]
    transc = top_alt.transcript
    print(u'Transcript: {}'.format(transc))

    # the target words list we should look at
    if lang == "zh":
        target_words = target_mono_zh
    else:
        target_words = target_mono_en

    # loop through all recognized words to find the target word
    # and return its start and end timestamps if found
    # otherwise return (0, 0)
    for word_info in top_alt.words:
        if word_info.word in target_words:
            start = word_info.start_time.seconds + word_info.start_time.nanos / 1.0e9
            end = word_info.end_time.seconds + word_info.end_time.nanos / 1.0e9
            return (start, end)
    
    return (0, 0)

print(find_taget_boundaries_mono(test_dir + "8_10_ch_n.wav", "zh"))
