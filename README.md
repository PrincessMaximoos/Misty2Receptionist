# Misty as a GPT enabled smart receptionist

REQUIRES INTERNET CONNECTION

----------------------------

## Install

Windows:

- Install python3 from the link below:
  https://www.python.org/downloads/
- Move it to Documents and run the exe

- Note: this is for Python 3.13 if you are using a different version change the file path below to match (e.g Python 2.7 -> \Python27\)
- Open Windows Powershell and copy the two commands below:
```
  cd C:\Users\<YOUR_USR>\AppData\Local\Programs\Python\Python313\Scripts
  pip install gpt4all typer misty-sdk websocket-client opencv-python-headless image speechrecognition pyttsx3 pyaudio
```

-------------------------------------------------------------------------------------------------------------------

Ubuntu:

- In a terminal run the following commands:
```
pip install gpt4all typer misty-sdk websocket-client opencv-python-headless image speechrecognition pyttsx3
sudo apt install espeak python3-pyaudio
```

-------------------------------------------------------------------------------------------------------------------

## Setup
- Power Misty on
- Plug an empty usb thumbdrive into PC and create a folder called '`misty`'
- When her eyes open fully, take her back cover off and insert a usb thumbdrive
- Wait 1 minute and not a moment less
- Plug usb back into pc and open the '`misty`' and then the `device_info.json` file in notepad
- `Ctrl + F` to find `ipAddress` and then copy number into the `IP_ADDRESS` constant
