#----Install----#
'''
Misty as a GPT enabled smart receptionist

pip install misty-sdk
pip install websocket-client
pip install opencv-python-headless image
pip install --upgrade gpt4all typer

https://github.com/nomic-ai/gpt4all?tab=readme-ov-file
# pick correct installer for your os

Nvidia Cuda
Linux:
sudo apt install nvidia-cuda-toolkit

Windows:
https://developer.nvidia.com/cuda-downloads?target_os=Windows&target_arch=x86_64&target_version=11&target_type=exe_local

'''

#----import mistyPy----#
from mistyPy.Robot import Robot
from mistyPy.GenerateRobot import RobotGenerator
from mistyPy.Events import Events

#----Data Store----#
#--import json--#
import json

#----QR----#
#--import cv2--#
import cv2

#--import base64--#
import base64

#----import threading----#
import threading

#----import GPT----#
from gpt4all import GPT4All


#----Global Declarable HELL----#
ids : list[dict] = {}
'''
List of IDs stored as a dictionary
'''

visitor_count = 0
'''
Number of unique visitors
'''


#----Global Functions----#
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
    # misty.Speak(mess)

def dev_inp(src : str = "") -> str:
    '''
    Similar to dev(). Returns User Input:
    -------------------------------------
    src : str / Where the message comes from. [Global | GPT | MistyGPT | QR ]
    '''

    print("{:^10}|".format(src), end = "")
    return input()

def drop() -> None:
    '''
    Drops a line using the dev line separator '|'
    '''

    print("{:^10}|".format(""))

def update_count() -> None:
    '''
    Updates the visitor_info file
    -----------------------------
    Appends ID list
    Updates number of visitors
    '''

    with open("output/visitor_info.txt", "a") as vis:
        vis.write("\n+-----------------------------------------+\n")
        string = "Number of Visitors: " + str(visitor_count) + '\n'
        for id in ids:
            for item in id.values():
                string += "{:<20}".format(str(item)) + '| '
            string += '\n'
        vis.write(string)
    vis.close()






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
    dev("QR", "Waiting for QR Code...")
    file : str = "output/qr_camera.png"

    while True:
        read = misty.TakePicture(True, "qr_check", 640, 480, False, True)

        with open(file, "wb") as f: # wb is important, standard write doesnt work (write as bytes maybe???)
            f.write(base64.b64decode(read.json()["result"]["base64"]))
        f.close()

        data = qr_search(file)

        if data == "quit":
            dev("QR", "Closing QR...")
            # break

            return "Null", "Null"

        elif data != "Error":
            id = id_check(data)
            if not id[0]:
                ids.append(id[1])
                dev("QR", "Valid ID Found", id[1]["Name"])
                visitor_count += 1
                update_count()
                dev("QR", "Visitor Count Incremented", str(visitor_count))

                return id[1]["Name"], ["IDNum"]

    # drop()
    # for id in ids:
    #     print("{:<7}|{:<20}|{:<20}|{:<20}".format("", id["Name"], id["Company"], id["IDNum"]))
    # print("{:<7}|Num of Visitors: {}".format("", visitor_count))
    # drop()


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

    '''

    global ids
    details : dict = {"Name" : "", "Company" : "", "IDNum" : 0}

    stringlist : list = data.split(', ')
    for string in stringlist:
        key_val : list[str] = string.split(': ')
        details[key_val[0]] = key_val[1]

    already_in_ids : bool = False
    for id in ids:
        if id["Name"] == details["Name"]:
            already_in_ids : bool = True

    return already_in_ids, details






#----GPT----#
def start_q_and_a(visitor_name : str, visitor_id : str):
    '''
    GPT Main Function.
    ------------------
    visitor_name : str [John Smith]
    visitor_id : str [42]

    Let the user ask questions.
    Provide them with contact information
    '''

    dev_speak("MistyGPT", "Hi {}, you can now ask me any questions about artificial intelligence or machine learning.".format(visitor_name))
    while True:
        dev("GPT", "Simulate visitor asking a question: ")
        question = dev_inp("Usr")  # Simulate voice recognition
        if not question.strip():
            continue
        
        print()
        answer = get_response(question)
        dev_speak("MistyGPT")
        print(answer)
        print()

        dev_speak("MistyGPT", "Do you have any more questions?")
        dev("GPT", "Simulate visitor response (yes/no): ")
        follow_up = dev_inp("Usr").strip().lower()
        if follow_up == "no":
            say_goodbye(visitor_name, visitor_id)
            break

def get_response(question : str) -> str:
    '''
    Generates a response.
    --------------------
    question : str [What is AI?]
    '''
    
    return model.generate("Without acknowledging this statement and keeping your answer short and concise. " + question)

def say_goodbye(visitor_name, visitor_id):
    '''
    Provide the user with contact information.
    ------------------------------------------
    visitor_name : str [John Smith]
    visitor_id : str [42]
    '''

    dev_speak("MistyGPT", "It was nice meeting you, {:<}. If you have further questions about AI or research collaboration, you can contact my master at b.b.bastaki@staffs.ac.uk.".format(visitor_name))
    dev_speak("MistyGPT", "Would you like me to repeat the email address?")
    dev("GPT", "Simulate visitor response (yes/no): ")

    repeat_email = dev_inp("Usr").strip().lower()
    if repeat_email == "yes":
        dev_speak("MistyGPT", "The email address is b.b.bastaki@staffs.ac.uk.")
    dev_speak("MistyGPT", "Bye for now! I will wait here for the next visitor.")





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
    
    model = GPT4All("Llama-3.2-1B-Instruct-Q4_0.gguf") # downloads / loads a 4.66GB LLM
    # model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf") # downloads / loads a 4.66GB LLM
    
    ip_address : str = "10.4.155.108"
    # misty : Robot = Robot(ip_address)

    with open("output/visitor_info.json") as f:
        file = json.load(f)
        ids = file["result"]
        visitor_count = file["num"]



    # thread = threading.Thread(target = qr_scan)
    # dev("Global", "Starting Thread")
    # thread.start()



    while True:
        dev("Global", "Starting QR Scan")
        # details : list = qr_main()
        
        details = "Max", 1

        dev("Global", "Starting GPT")
        dev()
        with model.chat_session():
            start_q_and_a(details[0], details[1])
        
        drop()
        for id in ids:
            print("{:<10}|{:<20}|{:<20}|{:<20}".format("", id["Name"], id["Company"], id["IDNum"]))
        print("{:<10}|Num of Visitors: {}".format("", visitor_count))
        drop()


    # thread.join()
    # dev("Global", "Thread closed")



