import os
import io

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

# set the directory here
# directory_str = "/Users/cynthiazhong/Google_Drive/Shen_1920LRAP/DATA/8/"
test_dir = "./test/"

# target words in monolingual english sentences
target_mono_en = ["bee", "beetle", "mountain", "lamp", "goat", "monkey", 
                "artichoke", "diamond", "leaf", "shark", "tulip", "bus", 
                "coat", "pipe", "cherry", "ball", "phone", "peach", "tie"]

# target words in monolingual chinese sentences
# target_mono_zh = ["苹果", "西瓜", "毛巾", "蓝宝石", "勺子", "杯子", "报纸", 
#                 "面包", "气球", "电视", "心", "礼物", "树", "糖", "袜子",
#                 "手机", "恐龙", "凳子"]

# since speech-to-text only separates chinese sentences into individual characters,
# i am using the first character in each target word instead
target_mono_zh = ["苹", "西", "毛", "蓝", "勺", "杯", "报", "面", "气", "电", "心", "礼", 
                "树", "糖", "袜", "手", "恐", "凳"]

def genearte_boundaries_file():
    """
    Generates two .txt files.

    First one is a table of target word boundaries, where each row contains
    audio_file_name target_word_start_timestamp target_word_end_timestamp (separated by tabs)
    for each audio file in the diirectory, which can be 
    fed into boundary-selector.praat for further Praat processing.

    Second one is a list of transcriptions that can be used as reference.
    """
    b = open("bounds-test.txt", "w+")
    t = open("transcriptions.txt", "w+")

    # list all files in directory
    directory = os.fsencode(test_dir)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        # if this is an audio w/o codeswitch
        if filename.endswith("n.wav"):
            # if audio is in english
            if filename.find("en") > -1:
                lang = "en_US"
            else:
                lang = "zh"
            find_taget_boundaries_mono(test_dir, filename, lang, b, t)
        # otherwise it's a code-switched audio
        # else:
        #     if filename.find("en") > -1:
        #         lang = "en_US"
        #         alt_lang = ["zh"]
        #     else:
        #         lang = "zh"
        #         alt_lang = ["en_US"]
        #     find_taget_boundaries_cs(test_dir, filename, lang, alt_lang, b, t)

    b.close()
    t.close()

# modified from Google speech-to-text API docs
def find_taget_boundaries_mono(directory, file_name, lang, b_file, t_file):
    """ Transcribe the given audio file synchronously,
    writes the transcription to t_file and 
    time offsets of the target word it contains to b_file. """

    client = speech.SpeechClient()

    audio_file_path = directory + file_name

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
    t_file.write(str(transc) + "\n")

    # the target words list we should look at
    if lang == "zh":
        target_words = target_mono_zh
    else:
        target_words = target_mono_en

    # loop through all recognized words to find the target word
    # and return its start and end timestamps if found
    # otherwise return (0, 0)
    start = 0.0
    end = 0.0

    for word_info in top_alt.words:
        if word_info.word in target_words:
            start = word_info.start_time.seconds + word_info.start_time.nanos / 1.0e9
            end = word_info.end_time.seconds + word_info.end_time.nanos / 1.0e9
    
    b_file_row = file_name + "\t" + str(start) + "\t" + str(end) + "\n"
    b_file.write(b_file_row)

genearte_boundaries_file()
