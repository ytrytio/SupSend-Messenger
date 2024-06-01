import requests
from datetime import datetime
import time
import threading
from rich import print as print_
from rich.panel import Panel
from rich.prompt import Prompt
from rich.spinner import Spinner
import keyboard
import os

#keyboard.add_hotkey("escape", lambda: print("Succesfuly escaped"))

#serverUrl = 'http://95.165.142.216:5000'
serverUrl = 'http://127.0.0.1:5000'

after = 0

def print_messages(messages):
    for message in messages:
        dt = datetime.fromtimestamp(message['time'])
        
        print_(Panel.fit(f"{message['text']}", title=f"{dt.strftime('%H:%M:%S')} - {message['name']}", title_align="left"))
        print(" ")
        






def recieve_msg():
    global after
    while True:
        response = requests.get(url=f'{serverUrl}/messages',
                                params={'after': after})
        messages = response.json()['messages']
        if messages:
            print_messages(messages)
            after = messages[-1]['time']

  

        time.sleep(1)


def send_msg():
    while True:
        text = input() 
        formated_text = text.split()
        formated_text = ''.join(formated_text)
        if formated_text == "":
            print("\033[FDon't write empty messages!")
            return send_msg()
        #print("\033[F\033[K")
        
        response = requests.post(url=f'{serverUrl}/send',
                                json={'name': name, 'text': text})


recieve = threading.Thread(target=recieve_msg, daemon=True)
send = threading.Thread(target=send_msg, daemon=True)


def back():
    keyboard.unhook_all_hotkeys()
    send._stop()
    recieve._stop()
    start()

def open_chat():
    os.system('clear')
    recieve.start()
    send.start()
    send.join()
    recieve.join()
    keyboard.add_hotkey("escape", back)
    keyboard.wait()

def start():
    os.system('clear')
    print_(Panel.fit("open \[chat name || settings]\nexit\nhotkeys", title="Available commands", title_align="center"))
    command = input("Command: ")
    if command[:4] == "open":
        chat_name = command[5:]
        Spinner('point', speed=1.0)

        
        open_chat()
    elif command == "exit": 
        exit()
    elif command == "hotkeys":    
        os.system('clear')
        print_(Panel.fit("Escape - back\nEnter - sends message when chat is open", title=f"Available hotkyes", title_align="center"))
        keyboard.add_hotkey("escape", back)
        keyboard.wait()
    else:    
        print("Incorrect command!")
        time.sleep(1)
        start()
    
os.system('clear')
name = input("Enter your name: ")




if __name__ == '__main__':
    start()
