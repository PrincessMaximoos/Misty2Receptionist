#----Install----#
'''
Misty as a GPT enabled smart receptionist

pip install --upgrade gpt4all typer

pip install misty-sdk websocket-client opencv-python-headless image

pip install pyaudio speechrecognition pyttsx3

https://github.com/nomic-ai/gpt4all?tab=readme-ov-file
# pick correct installer for your os

Linux:
sudo apt install nvidia-cuda-toolkit
sudo apt install espeak

Windows:
https://developer.nvidia.com/cuda-downloads?target_os=Windows&target_arch=x86_64&target_version=11&target_type=exe_local


Linux:

'''

#----import mistyPy----#
from mistyPy.Robot import Robot
from mistyPy.GenerateRobot import RobotGenerator
from mistyPy.Events import Events

#----Data Storage----#
import json

#----QR----#
import cv2
import base64

#----import time----#
import time

#----import GPT----#
from gpt4all import GPT4All

#----import text/speech/text----#
import speech_recognition as sr
import pyttsx3

#----Global Declarable HELL----#
ids : list = []

visitor_count : int = 0



#----Dev Functions----#
class dev_commands:
    '''
    Basic Developer commands for displaying and taking information
    --------------------------------------------------------------
    '''
    def __init__(self):
        pass

    def dev(self, src : str = "", mess : str = "", info : any = "") -> None:
        '''
        Formats the given input for debug purposes:
        -------------------------------------------
        src : str / Where the message comes from. [Global | GPT | MistyGPT | QR ]
        mess : str / The desired message output
        info : any / Blank, general purpose additional info

        "Dev | System Message            |"
        '''

        print("{:^10}|{:<100}|{:<}".format(src, mess, info))
    
    def dev_typeinp(self, src : str = "") -> str:
        '''
        Similar to dev(). Returns User Input:
        -------------------------------------
        src : str / Where the message comes from. [Global | GPT | MistyGPT | QR ]
        '''

        print("{:^10}|".format(src), end = "")
        return input()

    def update_count(self) -> None:
        '''
        Updates the visitor_info file
        -----------------------------
        Appends ID list
        Updates number of visitors
        '''

        with open("output/visitor_info.json", "w") as vis:
            json.dump({"result" : ids, "num" : visitor_count}, vis)

class dev_nomisty(dev_commands):
    '''
    Child class of dev_commands

    Used when Misty does *not* connect successfully
    -----------------------------------------------
    '''

    def __init__(self):
        super().__init__()


    def dev_speak(self, src : str = "", mess : str = "", info : any = "") -> None:
        '''
        Expanded dev() for speech.
        Formats the given input and uses text_to_speech:
        ------------------------------------------------------
        src : str / Where the message comes from. [Global | GPT | MistyGPT | QR ]
        mess : str / The desired message output
        info : any / Blank, general purpose additional info
        '''

        self.dev(src, mess, info)
        
        # text_to_speech(mess)

    def dev_inp(self, src : str = "") -> str:
        '''
        Similar to dev(). Returns User Speech:
        -------------------------------------
        src : str / Where the message comes from. [Global | GPT | MistyGPT | QR ]
        '''

        # print("{:^10}|".format(src), end = "")
        # text = speech_to_text()

        # print(text, end = "\n")
        text = self.dev_typeinp(src)

        return text

class dev_misty(dev_commands):
    '''
    Child class of dev_commands

    Used when Misty connects successfully and utilises her functions.
    -----------------------------------------------------------------
    '''

    def __init__(self):
        super().__init__()

    def dev_speak(self, src : str = "", mess : str = "", info : any = "") -> None:
        '''
        Expanded dev() for speech.
        Formats the given input and uses Misty Speech to Text:
        ------------------------------------------------------
        src : str / Where the message comes from. [Global | GPT | MistyGPT | QR ]
        mess : str / The desired message output
        info : any / Blank, general purpose additional info
        '''

        self.dev(src, mess, info)
        misty.Speak(mess)
        
    def dev_inp(self, src : str = "") -> str:
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
    
        # return self.dev_typeinp(src)

class dev_text(dev_commands):
    '''
    Text only version of the expanded dev_commands()
    ------------------------------------------------
    '''

    def __init__(self):
        super().__init__()

    def dev_speak(self, src : str = "", mess : str = "", info : any = "") -> None:
        '''
        Identical to dev() for when noise is not wanted.
        Formats the given input and outputs to the user:
        ------------------------------------------------------
        src : str / Where the message comes from. [Global | GPT | MistyGPT | QR ]
        mess : str / The desired message output
        info : any / Blank, general purpose additional info
        '''

        self.dev(src, mess, info)
    
    def dev_inp(self, src : str = "") -> str:
        '''
        Identical to dev_typeinp(). Returns User Input:
        -------------------------------------
        src : str / Where the message comes from. [Global | GPT | MistyGPT | QR ]
        '''

        return self.dev_typeinp(src)


#----QR Code Functions----#
def qr_main() -> list:
    '''
    Runs the QR Code algorithm:
    --------------------------
    Takes Picture,
    Searches for QR code.
    If valid QR and valid ID,
    Return the name and ID number.
    Otherwise start again.
    '''

    global visitor_count
    global ids
    dev.dev("QR", "Waiting for QR Code...")
    file : str = "output/qr_camera.png"

    while True:
        read = misty.TakePicture(True, "qr_check", 640, 480, False, True)
        

        with open(file, "wb") as f: # wb is important (write as bytes)
            f.write(base64.b64decode(read.json()["result"]["base64"]))
        f.close()

        data = qr_search(file)

        if data == "quit":
            dev.dev("QR", "Closing QR...")

            return "Null"

        elif data != "Error":
            id : list[any] = id_check(data)
            if not id[0]:
                ids.append(id[1])
                dev.dev("QR", "Valid ID Found", id[1]["Name"])
                visitor_count += 1
                dev.update_count()
                dev.dev("QR", "Visitor Count Incremented", str(visitor_count))

                return id[1]
            else:
                print("ID alreadyfound")

def qr_search(filename : str) -> str:
    '''
    Uses cv2 to search for a QR Code
    --------------------------------
    filename : str [output/qr_camera.png]

    Read image file, look for QR Code.
    If found, return the data.
    Otherwise, return an error.
    '''

    image = cv2.imread(filename)
    detector = cv2.QRCodeDetector()
    data, vertices_array, binary_qrcode = detector.detectAndDecode(image)

    if vertices_array is not None and data != "":
        return(data)
    else:
        return("Error")

def id_check(data : str) -> list:
    '''
    Check ID against ID list. Returns (whether in ids), (their details).
    ---------------------------------------------------------------
    data : str ["Name: John Smith, Company: Staffs, IDNum: 42"]

    Returns:
    already_in_ids : bool,
    details : dict

    '''

    global ids
    details : dict = {"Name" : "", "Company" : "", "IDNum" : visitor_count, "Amount": 1}

    stringlist : list = data.split(', ')
    for i in range(len(stringlist)):
        string = stringlist[i]
        key_val : list[str] = string.split(': ')
        details[key_val[0]] = key_val[1]

    already_in_ids : bool = False
    for id in ids:
        if id["Name"] == details["Name"]:
            already_in_ids : bool = True
            dev.dev("ID", "Already in IDs", f"{details["Name"]}, {details["Company"]}, {details['IDNum']}")
            id["Amount"] += 1
            details["Amount"] = id["Amount"]
            dev.dev("ID", "Incrementing Amount", f"{details["Amount"] - 1} -> {details["Amount"]}")
            id_rewrite()

    return already_in_ids, details

def id_append(id : list[dict]) -> list:
    '''
    Update the ID information
    '''
    global visitor_count
    global ids
    ids.append(id[1])
    dev.dev("QR", "Valid ID Found", id[1]["Name"])
    visitor_count += 1
    dev.update_count()
    dev.dev("QR", "Visitor Count Incremented", str(visitor_count))

    return id[1]["Name"], id[1]["IDNum"]

def id_rewrite() -> None:
    global ids
    with open("output/visitor_info.json", "w") as f:
        json.dump({"result" : ids, "num" : visitor_count}, f)

def greet(details : dict) -> list[str]:
    '''
    Gets the Preferred name of the user
    -----------------------------------
    '''
    global dev
    correct = False
    dev.dev_speak("QR", "Hi Visitor {}, what would you like me to call you?".format(details["IDNum"]))
    while not correct:
        name = dev.dev_inp("QR")
        dev.dev_speak("QR", f"Did you say {name}?")
        answer = dev.dev_inp("QR").strip().lower()
        if answer == "yes":
            details = name, details["Company"], details["IDNum"]
            correct = True
        else:
            dev.dev_speak("QR", "What would you like me to call you?")
    
    return details


#----GPT----#
def start_q_and_a(visitor_name : str, visitor_id : str, already_checked : bool) -> None:
    '''
    GPT Main Function.
    ------------------
    visitor_name : str [John Smith]
    visitor_id : str [42]

    Let the user ask questions.
    Provide them with contact information
    '''
    if already_checked:
        dev.dev_speak("MistyGPT", f"Hi {visitor_name}, It's nice to see you again. What can I help you with?")
    else:
        dev.dev_speak("MistyGPT", f"Hi {visitor_name}, you can now ask me any questions about artificial intelligence or machine learning. Just say 'Hey Misty' followed by your question.")
    
    while True:
        dev.dev("GPT", "Ask a question: ")
        question = dev.dev_inp("Usr")  # Simulate voice recognition
        if not question.strip():
            continue
        
        print()
        answer = get_response(question)
        dev.dev_speak("MistyGPT", answer)
        print()

        follow_up = ""
        while follow_up != "yes" and follow_up != "no":
            dev.dev_speak("MistyGPT", "If you have anymore questions say 'Hey Misty, I have more questions' otherwise say 'Hey Misty, I dont have anymore questions'")
            dev.dev("GPT", "Simulate visitor response (yes/no): ")
            follow_up = dev.dev_inp("Usr").strip().lower()
            if follow_up == "i dont have anymore questions":
                say_goodbye(visitor_name, visitor_id)
                return 0
            elif follow_up == "i have more questions":
                break
            else:
                dev.dev_speak("MistyGPT", "I'm sorry I didnt understand that.")

def get_response(question : str) -> str:
    '''
    Generates a response.
    --------------------
    question : str [What is AI?]
    '''

    return model.generate("Without acknowledging this statement and keeping your answer short and concise. " + question)

def say_goodbye(visitor_name, visitor_id) -> None:
    '''
    Provide the user with contact information.
    ------------------------------------------
    visitor_name : str [John Smith]
    visitor_id : str [42]
    '''

    dev.dev_speak("MistyGPT", "It was nice meeting you, {:<}. If you have further questions about AI or research collaboration, you can contact my boss at b.b.bastaki@staffs.ac.uk.".format(visitor_name))
    dev.dev_speak("MistyGPT", "If you would like me to repeat the email, say 'Hey Misty, can you repeat the email'")
    dev.dev("GPT", "Simulate visitor response: ")

    repeat_email = dev.dev_inp("Usr").strip().lower()
    if repeat_email == "can you repeat the email":
        dev.dev_speak("MistyGPT", "The email address is b.b.bastaki@staffs.ac.uk.")
    dev.dev_speak("MistyGPT", "Bye for now! I will wait here for the next visitor.")

def speech_to_text() -> str:
    # Create a Speech Recognition object
    r = sr.Recognizer()

    # Use the microphone as the input device
    mic = sr.Microphone()

    try:
        # Start listening for audio from the microphone
        with mic as source:
            audio = r.listen(source)

            # Try to recognize what was said
            text = r.recognize_google(audio)
            return text
    except:
        return ""
    
def audio_to_text(filepath : str) -> str:
    r = sr.Recognizer()
    with sr.AudioFile(filepath) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data)
        return text

def text_to_speech(text : str = "empty") -> None:
    engine = pyttsx3.init()
    engine.setProperty('rate', 150) # speed
    engine.say(text)
    engine.runAndWait()


#----Main Function----#
if __name__ == "__main__":
    '''
    Main Function.
    --------------
    Choose GPT model.

    Link to Misty.

    
    Begin Loop:

    Look for QR codes

    Greet and assist the user
    '''


    model = GPT4All("Llama-3.2-1B-Instruct-Q4_0.gguf") # less resource intensive model
    # model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf") # stronger model
    
    ip_address : str = "10.4.154.243"
    
    method = input("Do you wish to enter the text only interface?\n").strip().lower()
    if method == "no":
        try:
            misty : Robot = Robot(ip_address)
            dev = dev_misty()
            dev.dev("Global", "Misty Connected")
        except:
            dev = dev_nomisty()
            dev.dev("Global", "Misty Connection Failed")

    else:
        dev = dev_text()
        dev.dev("Global", "Text Only")
    
    try:
        f = open("output/visitor_info.json")
        file = json.load(f)
        ids = file["result"]
        visitor_count = file["num"]
    except:
        ids : list[dict] = [{"Name" : "Name", "Company" : "Company", "IDNum" : "IDNum"}, ]
        visitor_count = 0

        with open("output/visitor_info.json", "w") as f:
            json.dump({"result" : ids, "num" : visitor_count}, f)
        
        f = open("output/visitor_info.json")
        file = json.load(f)
        ids = file["result"]
        visitor_count = file["num"]

    while True:
        dev.dev("Global", "Starting QR Scan")

        if isinstance(dev, dev_misty):
            info : dict = qr_main()
        
        elif isinstance(dev, dev_nomisty):
            details : str = qr_search("qr_codes/max.png")
            id : list = id_check(details)
            if not id[0]:
                id_append(id)
            info = id[1]
            
        else:
            
            details : dict = dev.dev_typeinp(src = "UsrName"), dev.dev_typeinp(src = "UsrID"), dev.dev_typeinp(src = "UsrComp")
            id : list = id_check(f"Name: {details[0]}, Company: {details[2]}, IDNum: {details[1]}")
            id_append(id)
            info = id[1]


        dev.dev("Global", "Starting GPT")
        dev.dev()
        with model.chat_session():
            start_q_and_a(info["Name"], info["IDNum"], id[0])

        print()
        for id in ids:
            print("{:<10}|{:<20}|{:<20}|{:<20}|{:<20}".format("", id["Name"], id["Company"], id["IDNum"], id["Amount"]))
        print("{:<10}|Num of Visitors: {}\n".format("", visitor_count))

        f.close()
