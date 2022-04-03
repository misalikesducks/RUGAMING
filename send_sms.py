import os
#from twilio.rest import Client
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import requests
from bs4 import BeautifulSoup
# from selenium import webdriver 
# from selenium.webdriver.common.keys import Keys 
import time
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

app = Flask(__name__)
@app.route("/sms", methods=['GET', 'POST'])
def sms_greeting():
    body = request.values.get('Body', None)
    resp = MessagingResponse()
    body = re.sub(r'[^a-zA-Z0-9 ]', '', body)
    body = body.lower()
    ind = body.rfind("im")
    if(ind != -1): 
        meme = body[ind + 3:len(body)]
        resp.message("Hi " + meme + ", I'm dad")
        return str(resp)
    body = body.strip()

    #genre search 
    ind = body.rfind("top")
    if(ind != -1): 
        genre = body[ind + 4:len(body)]
        toplist = scrape2(genre)
        resp.message("1. " + toplist[0] + "\n2. " + toplist[1] + "\n3. " + toplist[2])
        return str(resp)
        
    #memes    
    if (body == "hi"):
        resp.message("Hello my name is Noobie! Are you lonely AND broke[n]? Play sum gamez then! : ) Please message me with the name of a PC game to get the lowest prices or a genre (enter \"Help Genre\" for the list of genres) to get the top 3 rated games for the specified genre.")
        return str(resp)
    elif (body == "help genre"):
        resp.message("TO SELECT: write \"top 'genre'\"\naction\nadventure\nfighting\nfirst person\nflight\nparty\nplatformer\npuzzle\nracing\nreal time\nrole playing\nsimulation\nsports\nstrategy\nthird person\nturn based\nwar game\nwrestling")
        return str(resp)
    elif (body == 'about'):
        resp.message("This bot was made during Spring 2022 HackRU by Connie Chen, Henry Lin, Brian Wang, and our fallen soldier Andy Li.")
        return str(resp)
    elif (body == 'can u be my friend'):
        stoopid = "Sure, visit me here: shorturl.at/hzIT2"
        resp.message(stoopid)
        return str(resp)
    elif (body == 'f'):
        resp.message("FFFFFFFFFF\nF\nF\nF\nFFFFFFF\nF\nF\nF\nF")
        return str(resp)
    elif (body == 'hi dad'):
        resp.message("Are ya winning son?")
        return str(resp)
    elif (body == 'yes'):
        resp.message("I'm proud of you my very biological son.")
        return str(resp)
    else: 
        resp.message(sms_reply(body))
    return str(resp)

def sms_reply(game_message):
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number    
    bod = re.sub(r'[^a-zA-Z0-9]', '', game_message)
    title = bod
    bod = bod.replace("1", "i")
    bod = bod.replace("2", "ii")
    bod = bod.replace("3", "iii")
    bod = bod.replace("4", "iv")
    bod = bod.replace("5", "v")
    bod = bod.replace("6", "vi")
    bod = bod.replace("7", "vii")
    bod = bod.replace("8", "viii")
    bod = bod.replace("9", "ix")
    body = bod.lower()

    # Start our TwiML response
    #resp = MessagingResponse()
    price, location, link = scraping(body)
    #lister = scrape2("adventure")
    wordy = " on sale for: "
    stra = title + wordy + price + " at: " + location + " " + link 
    # Determine the right reply for this message
    #resp.message(stra)
    #return str(resp)
    return stra

def scraping(game_name):

    #s = Service(r'C:/Users/cool4/Downloads/chromedriver_win32')
    #driver = webdriver.Chrome(executable_path=r'C:/Users/cool4/Downloads/chromedriver_win32/chromedriver.exe')
    s = Service('/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=s)

    driver.get('https://isthereanydeal.com/#/filter:&search/%s'%game_name)
    time.sleep(2) 
    SCROLL_PAUSE_TIME = 0.4


    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


    pagesource = driver.page_source

    #page = requests.get('https://isthereanydeal.com') # Getting page HTML through request
    soup = BeautifulSoup(pagesource, 'lxml') # Parsing content using beautifulsoup
    #a = soup.select("a[href^=?game_name]")
    #ssprint(a)
    price = soup.find('a', {'data-evt' : '["shop","click","%s"]'%(game_name)})
    if (price == None):
        return
    
    try: 
        rest = price.find_all_next('a', {'data-evt' : '["shop","click","%s"]'%(game_name)})
        place = rest[len(rest)-1]['data-slc']
        link = rest[len(rest)-1]['href']
        return rest[len(rest)-1].text, place , link
    except: 
        rest = price
        place = rest['data-slc']
        link = rest['href']
        return(rest.text, place , link)

def scrape2(genre):
    s = Service('/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=s)

    driver.get('https://www.metacritic.com/browse/games/genre/metascore/%s/all?view=detailed'%genre)
    time.sleep(2) 
    SCROLL_PAUSE_TIME = 0.4


    # print('https://www.metacritic.com/browse/games/genre/metascore/%s/all?view=detailed'%genre)
    # page = requests.get('https://www.metacritic.com/browse/games/genre/metascore/%s/all?view=detailed'%genre)
    # print('https://www.metacritic.com/browse/games/genre/metascore/%s/all?view=detailed'%genre)
    # soup = BeautifulSoup(page.content, 'html.parser')
        
    pagesource = driver.page_source
    soup = BeautifulSoup(pagesource, 'lxml')

    all = soup.find_all('span', {'class' : 'title numbered'})
    top_three = []
    for stuff in all: 
        if(stuff.text.strip() == '1.'): 
            top_three.append(stuff.find_next_sibling("a").h3.text)
        elif(stuff.text.strip() == '2.'):
            top_three.append(stuff.find_next_sibling("a").h3.text)
        elif(stuff.text.strip() == '3.'):
            top_three.append(stuff.find_next_sibling("a").h3.text)
    return top_three


if __name__ == "__main__":
    app.run(debug=True)
    