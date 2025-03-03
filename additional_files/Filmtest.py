from mistyPy.Robot import Robot
from mistyPy.GenerateRobot import RobotGenerator
from mistyPy.Events import Events
import speech_recognition as sr
import base64
import time

from gpt4all import GPT4All
model = GPT4All("Llama-3.2-1B-Instruct-Q4_0.gguf")

misty = Robot("10.4.154.243")

def ask(question : str = "Say I'm sorry, I didn't understand that.") -> str:
    with model.chat_session():
        return model.generate("Without acknowledging this statement and keeping your answer short and concise. " + question)
    model.generate()

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
    misty.CaptureSpeech(True, requireKeyPhrase = True)
    fail : str = "Failed"
    i = 0
    while fail == "Failed" or i < 30:
        b64 : str = misty.GetAudioFile("capture_HeyMisty.wav", True)
        fail = b64.json()["status"]
        i += 1

    dev("Test", fail)

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
        text = dev_inp("Usr")
        response = ask(text)
        dev_speak("Misty", response)
        sleep = 1
        for i in range(len(response.split(" ")) / 4 / 8):
            misty.MoveHead(yaw = 30)
            misty.MoveArm("left", 90)
            time.sleep(sleep)
            misty.MoveArm("right", 45)
            time.sleep(sleep)
            
            misty.MoveHead(yaw = -15)
            misty.MoveArm("left", 0)
            time.sleep(sleep)
            misty.MoveArm("right", 0)
            time.sleep(sleep)

            misty.MoveHead(yaw = -30)
            misty.MoveArm("left", 45)
            time.sleep(sleep)
            misty.MoveArm("right", 90)
            time.sleep(sleep)

            misty.MoveHead(yaw = 0)
            misty.MoveArm("left", 0)
            time.sleep(sleep)
            misty.MoveArm("right", 0)
            time.sleep(sleep)

    except:
        dev("Misty", "Error")