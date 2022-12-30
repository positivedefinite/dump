import pyautogui as pg
import time, tkinter
from bs4 import BeautifulSoup

time.sleep(5)

#config
GPT_RESPONSE_WAIT = 60

#pg.moveTo(1090, 2045) #for two screens
pg.moveTo(789, 965) #for one screen

pg.click()

def send_to_whatsapp(query):
    print('send_to_whatsapp')
    pg.hotkey('ctrl','2')
    time.sleep(0.3)
    pg.click()
    pg.typewrite(query)
    pg.press('enter')

def read_from_whatsapp(output_file:str="./data/question.txt"):
    print('read_from_whatsapp')
    pg.hotkey('ctrl','2')
    time.sleep(0.3)
    pg.press('f12')
    time.sleep(1)
    pg.press('tab')
    time.sleep(1)
    #div = f'/html/body/div/div/div[1]/main/div[1]/div/div/div[2]/div/div[2]/div[1]/div/div'
    #        /html/body/div/div/div[1]/main/div[1]/div/div/div/div[4]/div/div[2]/div[1]/div/div
    div = f"/html/body/div[1]/div/div/div[4]/div/div[2]/div/div[2]/div[3]"
    pg.typewrite(div)
    time.sleep(1)
    pg.press('enter')

    for _ in range(3):
        time.sleep(0.3)
        pg.press("tab")
    time.sleep(0.5)

    pg.hotkey('ctrl', 'c')
    clipboard_contents = tkinter.Tk().clipboard_get()

    with open(output_file, "w") as f:
        f.write(clipboard_contents)
    cleaned_messages = clipboard_contents
    
    soup = BeautifulSoup(cleaned_messages, 'html.parser')
    spans = soup.find_all('span', {'class': 'copyable-text'})
    message = spans[-1].text
    #print(cleaned_messages)

    pg.press('f12')
    time.sleep(0.5)
    return message

def check_if_message_updated(message, last_whatsapp_message, last_response):
    print('check_if_message_updated')
    return message if message != last_whatsapp_message and message[:10] != last_response[:10] else ""

def prompt_GPT(query:str, output_file:str="./data/answer.txt"):
    print('prompt_GPT')
    # Assumes ChatGPT is open on the first screen 
    pg.hotkey('ctrl','1')
    time.sleep(1)
    pg.click() #we expect the cursor to be over the searchbar

    pg.typewrite(query)
    pg.press('enter')
    time.sleep(GPT_RESPONSE_WAIT)

    pg.press('f12')
    time.sleep(1)
    pg.press('tab')
    time.sleep(1)
    #div = f'/html/body/div/div/div[1]/main/div[1]/div/div/div[2]/div/div[2]/div[1]/div/div'
    #        /html/body/div/div/div[1]/main/div[1]/div/div/div/div[4]/div/div[2]/div[1]/div/div
    div = f"/html/body/div/div/div[1]/main/div[1]/div/div"
    pg.typewrite(div)
    time.sleep(1)
    pg.press('enter')

    for _ in range(3):
        time.sleep(0.3)
        pg.press("tab")
    time.sleep(0.5)

    pg.hotkey('ctrl', 'c')
    clipboard_contents = tkinter.Tk().clipboard_get()
    soup = BeautifulSoup(clipboard_contents, 'html.parser')
    spans = soup.find_all('div', {'class': "min-h-[20px]"})
    clipboard_contents = spans[-1].text

    pg.press('f12')
    time.sleep(0.5)
    return clipboard_contents

last_whatsapp_message = ''
last_response = ''
messages = ""
while True:
    print('running the main loop')
    if messages == "": 
        print('last message empty, reading whatsapp')
        last_whatsapp_message = read_from_whatsapp()

    messages = read_from_whatsapp()
    message = check_if_message_updated(messages, last_whatsapp_message, last_response)

    if message != "":
        print('last message not empty, querying GPT')
        answer = prompt_GPT(message)
        last_response = answer
        last_whatsapp_message = message
        send_to_whatsapp(answer)
    else:
        print('last message did not change, doing nothing')

    time.sleep(10)
