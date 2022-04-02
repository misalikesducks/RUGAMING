

import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'AC0aff8479ad4ec2e26cb58a762f5107d3'
auth_token ='4b32cd3644475dcdcc33bd16ce5350be'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="brian's face is so big u can play mahjong on it",
                     from_='+1938-666-9586',
                     to='+17327738287'
                 )

print(message.sid)