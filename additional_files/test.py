from gpt4all import GPT4All
model = GPT4All("Llama-3.2-1B-Instruct-Q4_0.gguf") # downloads / loads a 4.66GB LLM

def ask(question):
    with model.chat_session():
        return model.generate("Without acknowledging this statement and keeping your answer short and concise. " + question)



# def update_count():
#     with open("output/visitor_info.txt", "a") as vis: # wb is important, standard write doesnt work (write as bytes maybe???)
#         vis.write("\n+-----------------------------------------+\n")
#         string = "Number of Visitors: " + str(visitor_count) + '\n'
#         for id in ids:
#             for item in id.values():
#                 string += "{:<20}".format(str(item)) + '| '
#             string += '\n'
#         vis.write(string)
#     vis.close()

# ids : list[dict] = [{"Name" : "Name", "Company" : "Company", "IDNum" : "IDNum"}, 
#                     {"Name" : "Max McGill", "Company" : "Staffs", "IDNum" : "0"}, 
#                     {"Name" : "Benhur Bastaki", "Company" : "Staffs", "IDNum" : "1"}]
# visitor_count = 2


# update_count()



# import json

# with open("output/visitor_info.json") as f:
#     test = json.load(f)
#     print(test["num"])



# ids : list[dict] = [{"Name" : "Name", "Company" : "Company", "IDNum" : "IDNum"}, ]
# visitor_count = 0

# import json

# with open("output/visitor_info.json", "w") as f:
#     json.dump({"result" : ids, "num" : visitor_count}, f)

# import speech_recognition as sr

# while True:
#     r = sr.Recognizer()
#     mic = sr.Microphone()

#     try:
#         with mic as source:
#             print("Listening...")
#             audio = r.listen(source)

#             text = r.recognize_google(audio)
#             print(f"Recognized: {text}")

#     except sr.UnknownValueError:
#         print("Speech recognition could not understand your input")


# import pyttsx3

# def text_to_speech(text):
#     engine = pyttsx3.init()
#     engine.setProperty('rate', 150) # speed
#     engine.say(text)
#     engine.runAndWait()

# text_to_speech("hello world")

# from pocketsphinx import LiveSpeech
# for phrase in LiveSpeech(): print(phrase)

from mistyPy.Robot import Robot
from mistyPy.GenerateRobot import RobotGenerator
from mistyPy.Events import Events
import speech_recognition as sr
import base64
import time

misty = Robot("10.4.154.243")

def dev(src : str = "", mess : str = "", info : any = "") -> None:
    '''
    Formats the given input for debug purposes:
    -------------------------------------------
    src : str / Where the message comes from. [Global | GPT | MistyGPT | QR ]
    mess : str / The desired message output
    info : any / Blank, general purpose additional info

    "Dev | System Message            |"
    '''

    print("{:^10}|{:<100}|{:<}".format(src, mess, info))

def dev_speak(src : str = "", mess : str = "", info : any = "") -> None:
    '''
    Expanded dev() for speech.
    Formats the given input and uses Misty Speech to Text:
    ------------------------------------------------------
    src : str / Where the message comes from. [Global | GPT | MistyGPT | QR ]
    mess : str / The desired message output
    info : any / Blank, general purpose additional info
    '''

    dev(src, mess, info)
    misty.Speak(mess)

def dev_inp(src : str = "") -> str:
    '''
    Similar to dev(). Returns User Input:
    -------------------------------------
    src : str / Where the message comes from. [Global | GPT | MistyGPT | QR ]
    '''

    print("{:^10}|".format(src), end = "")
    misty.DeleteAudio("capture_HeyMisty.wav")
    misty.CaptureSpeech(True, requireKeyPhrase=True)
    fail = "Failed"
    while fail == "Failed":
        b64 = misty.GetAudioFile("capture_HeyMisty.wav", True)
        fail = b64.json()["status"]

    with open("output/audio.wav", "wb") as f:
        f.write(base64.b64decode(b64.json()["result"]["base64"]))
    f.close()

    response = audio_to_text("output/audio.wav")
    return response

def audio_to_text(filepath : any):
    r = sr.Recognizer()
    with sr.AudioFile(filepath) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data)
        return text

while True:
    try:
        dev_speak("", ask(dev_inp("Test")))

    except:
        dev("Fail", "Error")