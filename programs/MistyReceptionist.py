#----Install----#
'''
pip install misty sdk
pip install websocket-client
pip install opencv-python-headless image
pip install PIL
pip install --upgrade gpt4all typer

https://github.com/nomic-ai/gpt4all?tab=readme-ov-file
# pick correct installer for your os

sudo apt install nvidia-cuda-toolkit

'''

#----import mistyPy----#
from mistyPy.Robot import Robot
from mistyPy.GenerateRobot import RobotGenerator
from mistyPy.Events import Events

#----QR----#
#--import requests--#
import requests

#--import cv2--#
import cv2

#--import PIL--#
from PIL import Image

#--import base64--#
import base64

#----import threading----#
import threading

#----import GPT----#
from gpt4all import GPT4All


#----Global Declarable HELL----#
ids : list[dict] = [{"Name" : "Name", "Company" : "Company", "IDNum" : "IDNum"}]
visitor_count = 0


#----Global Functions----#
def dev(src : str = "Dev", mess : str = "", returns : any = ""):
    print("{:<7}|{:<45}|{:<}".format(src, mess, returns))

def drop():
    print("{:<7}|".format(""))







#----QR Code Functions----#
def qr_scan() -> list:
    global visitor_count
    global ids
    dev("QR", "Waiting for QR Code...")
    file = "output/qr_camera.png"

    while True:
        read = misty.TakePicture(True, "qr_check", 640, 480, False, True)

        with open(file, "wb") as f: # wb is important, standard write doesnt work (write as bytes maybe???)
            f.write(base64.b64decode(read.json()["result"]["base64"]))
        f.close()

        data = qr_read(file)

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
                dev("QR", "Visitor Count Incremented", str(visitor_count))

                return id[1]["Name"], ["IDNum"]

    # drop()
    # for id in ids:
    #     print("{:<7}|{:<20}|{:<20}|{:<20}".format("", id["Name"], id["Company"], id["IDNum"]))
    # print("{:<7}|Num of Visitors: {}".format("", visitor_count))
    # drop()


def qr_read(filename : str) -> str:

    image = cv2.imread(filename)

    detector = cv2.QRCodeDetector()

    data, vertices_array, binary_qrcode = detector.detectAndDecode(image)

    if vertices_array is not None and data != "":
        return(data)
    else:
        return("Error")

def id_check(data : str) -> list:
    global ids
    details : dict = {"Name" : "", "Company" : "", "IDNum" : 0}

    stringlist : list = data.split(', ')
    for string in stringlist:
        sectionlist = string.split(': ')
        details[sectionlist[0]] = sectionlist[1]

    already_in_ids = False
    for id in ids:
        if id["Name"] == details["Name"]:
            already_in_ids = True

    return already_in_ids, details






#----GPT----#
def get_response(question : str) -> str:
    return model.generate(question)

def start_q_and_a(visitor_name : str, visitor_id : int):
    dev("GPT", "You can now ask me any questions about artificial intelligence or machine learning.")
    while True:
        dev("GPT", "Simulate visitor asking a question: ")
        question = input()  # Simulate voice recognition
        if not question.strip():
            continue

        answer = get_response(question)
        print(answer)

        dev("GPT", "Do you have any more questions?")
        dev("GPT", "Simulate visitor response (yes/no): ")
        follow_up = input().strip().lower()
        if follow_up == "no":
            say_goodbye(visitor_name, visitor_id)
            break

def say_goodbye(visitor_name, visitor_id):
    dev("GPT", "It was nice meeting you, {visitor_name}. If you have further questions about AI or research collaboration, you can contact my master at email@example.com.")
    dev("GPT", "Would you like me to repeat the email address?")
    dev("GPT", "Simulate visitor response (yes/no): ")

    repeat_email = input().strip().lower()
    if repeat_email == "yes":
        dev("GPT", "The email address is b.b.bastaki@staffs.ac.uk.")
    dev("GPT", "Bye for now! I will wait here for the next visitor.")





#----Main Function----#
if __name__ == "__main__":
    
    model = GPT4All("Llama-3.2-1B-Instruct-Q4_0.gguf") # downloads / loads a 4.66GB LLM
    
    ip_address : str = "10.4.155.108"
    # misty : Robot = Robot(ip_address)

    # thread = threading.Thread(target = qr_scan)
    # dev("Global", "Starting Thread")
    # thread.start()

    dev("Global", "Starting QR Scan")
    # details : list = qr_scan()
    details = "Max", 1

    dev("Global", "Starting GPT")
    with model.chat_session():
        start_q_and_a(details[0], details[1])

    # thread.join()
    # dev("Global", "Thread closed")



