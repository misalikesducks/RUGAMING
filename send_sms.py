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
    body = re.sub(r'[^a-zA-Z0-9]', '', s)
    body = body.lower()

    # Start our TwiML response
    resp = MessagingResponse()
    price = scraping(body)
    wordy = "Price: "
    stra = wordy + price
    # Determine the right reply for this message
    resp.message(stra)
    return str(resp)

def scraping(game_name):
    page = requests.get('https://isthereanydeal.com') #Getting page HTML through request
    soup = BeautifulSoup(page.content, 'html.parser') # Parsing content using beautifulsoup
 
    all_divs = soup.find('a', {'data-evt' : '["shop","click","%s"]'%(game_name)})
    try: 
        rest = all_divs.find_all_next('a', {'data-evt' : '["shop","click","%s"]'%(game_name)})
        return rest[len(rest)-1].text
    except: 
        rest = all_divs
        return rest.text

if __name__ == "__main__":
    app.run(debug=True)


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
#account_sid = 'AC0aff8479ad4ec2e26cb58a762f5107d3'
#auth_token ='4b32cd3644475dcdcc33bd16ce5350be'
#client = Client(account_sid, auth_token)

#message = client.messages \
#                .create(
#                     body="PTSD",
#                     from_='+1938-666-9586',
#                     to='+7328232741'
#                 )

#print(message.sid)