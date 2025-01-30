#----Install----#
#pip install misty sdk
#pip install websocket-client
#pip install opencv-python-headless image
#pip install PIL

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


#----Global Declarable HELL----#
ids : list[dict] = [{"Name" : "Name", "Company" : "Company", "IDNum" : "IDNum"}]
visitor_count = 0


#----Global Functions----#
def dev(src : str = "Dev", mess : str = "", returns : any = ""):
    print("{:<7}|{:<45}|{:<}".format(src, mess, returns))


#----QR Code Functions----#
def qr_scan():
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
            break
        elif data != "Error":
            id = id_check(data)
            if not id[0]:
                ids.append(id[1])
                dev("QR", "Valid ID Found", id[1]["Name"])
                visitor_count += 1
                dev("QR", "Visitor Count Incremented", str(visitor_count))

    print()
    for id in ids:
        print("{:<20}|{:<20}|{:<20}".format(id["Name"], id["Company"], id["IDNum"], ))
    print("\nNum of Visitors: {}".format(visitor_count))


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


if __name__ == "__main__":
    ip_address : str = "10.4.155.169"
    misty : Robot = Robot(ip_address)

    thread = threading.Thread(target = qr_scan)

    dev("Global", "Starting Thread")
    thread.start()

    thread.join()
    dev("Global", "Thread closed")



