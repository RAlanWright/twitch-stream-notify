import requests
from twilio.rest import Client
# Twilio SID & Auth Token
client = Client("StringOfAlphanumeric",
                "StringOfAlphanumeric")

# Change username to the streamer you want
TwitchUser = "TwitchUserName"
endpoint = "https://api.twitch.tv/helix/streams?"

# Twitch Client ID
headers = {"Client-ID": "StringOfAlphanumeric"}
params = {"user_login": TwitchUser}
response = requests.get(endpoint, params=params, headers=headers)
json_response = response.json()

sentFromNumber = "+19011234567"
sentToNumber = "+19012345678"

streams = json_response.get('data', [])


def is_active(stream): return stream.get('type') == 'live'


streams_active = filter(is_active, streams)
at_least_one_stream_active = any(streams_active)

# To prevent text spamming
# Comment this out to test SMS
last_messages_sent = client.messages.list(limit=1)
if last_messages_sent:
    last_message_id = last_messages_sent[0].sid
    last_message_data = client.messages(last_message_id).fetch()
    last_message_content = last_message_data.body
    online_notified = "LIVE" in last_message_content
    offline_notified = not online_notified
else:
    online_notified, offline_notified = False, False

print(at_least_one_stream_active)  # Print out True/False
print('Sending SMS to EndUser...')

# Comment this out to check whether SMS was previously sent for
# The Live or Offline depending on each case
if at_least_one_stream_active and not online_notified:
    client.messages.create(
        to=sentToNumber, from_=sentFromNumber, body=f'{TwitchUser}\'s STREAM IS LIVE!')
    print('Finished sending SMS!  \nProgram will now exit...')
if not at_least_one_stream_active and not offline_notified:
    client.messages.create(
        to=sentToNumber, from_=sentFromNumber, body=f'{TwitchUser}\'s STREAM IS OFFLINE!')
if at_least_one_stream_active and online_notified or offline_notified:
    print('Unable to send SMS.  Message limit reached...  \nProgram will now exit...')

# Un-comment this to test sending SMS
# if (at_least_one_stream_active):
#     client.messages.create(
#         to=sentToNumber, from_=sentFromNumber, body=f'{TwitchUser}\'s STREAM IS LIVE!')
# else:
#     client.messages.create(
#         to=sentToNumber, from_=sentFromNumber, body=f'{TwitchUser}\'s STREAM IS OFFLINE!')
# print('Finished sending SMS!  \nProgram will now exit...')
