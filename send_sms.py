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

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])


def sms_reply():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    s = request.values.get('Body', None)
    bod = re.sub(r'[^a-zA-Z0-9]', '', s)
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
    resp = MessagingResponse()
    price, location, link = scraping(body)
    wordy = " on sale for: "
    stra = title + wordy + price + " at: " + location + " " + link 
    # Determine the right reply for this message
    resp.message(stra)
    return str(resp)

def scraping(game_name):
    page = requests.get('https://isthereanydeal.com') #Getting page HTML through request
    soup = BeautifulSoup(page.content, 'html.parser') # Parsing content using beautifulsoup
 
    price = soup.find('a', {'data-evt' : '["shop","click","%s"]'%(game_name)})
    
    try: 
        rest = price.find_all_next('a', {'data-evt' : '["shop","click","%s"]'%(game_name)})
        place = rest['data-slc']
        link = rest['href']
        return rest[len(rest)-1].text, place, link 
    except: 
        rest = price
        place = rest['data-slc']
        link = rest['href']
        return rest.text, place, link

if __name__ == "__main__":
    app.run(debug=True)