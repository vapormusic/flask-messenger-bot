import os
import sys
import json
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import requests
from flask import Flask, request

app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["600 per minute", "8 per second"],
)

verify_token = "mfechat"
# token to send messages through facebook messenger
access_token = "EAAMkcdpZBH38BAMwpgUZCnemuTZB65vpdMdg8DkTPXVbBw7XoX9C7GuE3kbcSTmn6vuRPwmUZB7zqunglXvhGscPtvlmFsGjpTDkPFn4gUGKWKFVrSPi5aAuHT0B9YEnFTK0LAsNjguKw6OyABvKbcwn3SH2NZAfct8q2EAk9ywtJWo3CzM9G"

verify_token_neu = "helloworld"
# token to send messages through facebook messenger
access_token_neu = "EAACZBVPYCHFsBAE3UReU3O6q0ZAadu6IQZB4l1ZAFgZAlVkRbQviZCigGZBwGEoatKm6hZApVl29EhN7brCubU5eTwZCDj6CJc73UzLixUBiGjf0aZCLGHrxht3LVVWuSDOAowsWlZAZASwsbyvIVmbrXuVpyn2o7mVrWUTW9mrAzwqCEMk59zFTQvSY"



list = []


@app.route('/neu', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == verify_token_neu:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/neu', methods=['POST'])   
def webhook():
    # endpoint for processing incoming messaging events

    data = json.loads(request.data.decode('utf-8'))
    print(data)
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

       # make sure this is a page subscription

    for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):     # someone sent us a message
                    received_message(request.data, messaging_event, 2)

                elif messaging_event.get("delivery"):  # delivery confirmation
                    pass
                    # received_delivery_confirmation(messaging_event)

                elif messaging_event.get("optin"):     # optin confirmation
                    pass
                    # received_authentication(messaging_event)

                elif messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    received_message2(request.data, 2)

                else:    # uknown messaging_event
                    pass

    return "ok", 200






@app.route('/mfe', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == verify_token:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/mfe', methods=['POST'])   
def webhook():
    # endpoint for processing incoming messaging events

    data = json.loads(request.data.decode('utf-8'))
    print(data)
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

       # make sure this is a page subscription

    for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):     # someone sent us a message
                    received_message(request.data, messaging_event,1)

                elif messaging_event.get("delivery"):  # delivery confirmation
                    pass
                    # received_delivery_confirmation(messaging_event)

                elif messaging_event.get("optin"):     # optin confirmation
                    pass
                    # received_authentication(messaging_event)

                elif messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    received_message2(request.data, 1)

                else:    # uknown messaging_event
                    pass

    return "ok", 200


def received_message(event2, event, server):
   if "text" in event["message"]:
        message_text = event["message"]["text"]

        # parse message_text and give appropriate response
        if message_text == 'image':
           pass

        elif message_text == 'file':
            pass

        elif message_text == 'audio':
            pass

        elif message_text == 'video':
            pass

        elif message_text == 'button':
            pass

        elif message_text == 'generic':
            pass

        elif message_text == 'share':
            pass
        else:
           if server == 1: 
            response = requests.post('http://localhost:5006/webhooks/facebook/webhook', event2)
           else:
            response = requests.post('http://localhost:5005/webhooks/facebook/webhook', event2)  
           print(str(response.text))
   
def received_message2(event,server):
    if server == 1:
     response = requests.post('http://localhost:5006/webhooks/facebook/webhook', event)
    else: 
     response = requests.post('http://localhost:5005/webhooks/facebook/webhook', event)  
    print(str(response.text))

# Message event functions
async def send_text_message(recipient_id, message_text):

    # encode('utf-8') included to log emojis to heroku logs
    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text.encode('utf-8')))
    
    message_data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })

    call_send_api(message_data)


# def send_generic_message(recipient_id):
#
#     message_data = json.dumps({
#         "recipient": {
#             "id": recipient_id
#         },
#         "message": {
#             "attachment": {
#                 "type": "template",
#                 "payload": {
#                     "template_type": "generic",
#                     "elements": [{
#                         "title": "rift",
#                         "subtitle": "Next-generation virtual reality",
#                         "item_url": "https://www.oculus.com/en-us/rift/",
#                         "image_url": "http://messengerdemo.parseapp.com/img/rift.png",
#                         "buttons": [{
#                             "type": "web_url",
#                             "url": "https://www.oculus.com/en-us/rift/",
#                             "title": "Open Web URL"
#                         }, {
#                             "type": "postback",
#                             "title": "Call Postback",
#                             "payload": "Payload for first bubble",
#                         }],
#                     }, {
#                         "title": "touch",
#                         "subtitle": "Your Hands, Now in VR",
#                         "item_url": "https://www.oculus.com/en-us/touch/",
#                         "image_url": "http://messengerdemo.parseapp.com/img/touch.png",
#                         "buttons": [{
#                             "type": "web_url",
#                             "url": "https://www.oculus.com/en-us/touch/",
#                             "title": "Open Web URL"
#                         }, {
#                             "type": "postback",
#                             "title": "Call Postback",
#                             "payload": "Payload for second bubble",
#                         }]
#                     }]
#                 }
#             }
#         }
#     })
#
#     log("sending template with choices to {recipient}: ".format(recipient=recipient_id))
#
#     call_send_api(message_data)
#
#
# def send_image_message(recipient_id):
#
#     message_data = json.dumps({
#         "recipient": {
#             "id": recipient_id
#         },
#         "message": {
#             "attachment": {
#                 "type":"image",
#                 "payload":{
#                     "url":"http://i.imgur.com/76rJlO9.jpg"
#                 }
#             }
#         }
#     })
#
#     log("sending image to {recipient}: ".format(recipient=recipient_id))
#
#     call_send_api(message_data)
#
#
# def send_file_message(recipient_id):
#
#     message_data = json.dumps({
#         "recipient": {
#             "id": recipient_id
#         },
#         "message": {
#             "attachment": {
#                 "type":"file",
#                 "payload":{
#                     "url":"http://ee.usc.edu/~redekopp/ee355/EE355_Syllabus.pdf"
#                 }
#             }
#         }
#     })
#
#     log("sending file to {recipient}: ".format(recipient=recipient_id))
#
#     call_send_api(message_data)
#
#
# def send_audio_message(recipient_id):
#
#     message_data = json.dumps({
#         "recipient": {
#             "id": recipient_id
#         },
#         "message": {
#             "attachment": {
#                 "type":"audio",
#                 "payload":{
#                     "url":"http://www.stephaniequinn.com/Music/Allegro%20from%20Duet%20in%20C%20Major.mp3"
#                 }
#             }
#         }
#     })
#
#     log("sending audio to {recipient}: ".format(recipient=recipient_id))
#
#     call_send_api(message_data)
#
#
# def send_video_message(recipient_id):
#
#     message_data = json.dumps({
#         "recipient": {
#             "id": recipient_id
#         },
#         "message": {
#             "attachment": {
#                 "type":"video",
#                 "payload":{
#                     "url":"http://techslides.com/demos/sample-videos/small.mp4"
#                 }
#             }
#         }
#     })
#
#     log("sending video to {recipient}: ".format(recipient=recipient_id))
#
#     call_send_api(message_data)
#
#
# def send_button_message(recipient_id):
#
#     message_data = json.dumps({
#         "recipient": {
#             "id": recipient_id
#         },
#         "message": {
#             "attachment": {
#                 "type":"template",
#                 "payload":{
#                     "template_type":"button",
#                     "text":"What do you want to do next?",
#                     "buttons":[
#                     {
#                         "type":"web_url",
#                         "url":"https://www.google.com",
#                         "title":"Google"
#                     },
#                     {
#                         "type":"postback",
#                         "title":"Call Postback",
#                         "payload":"Payload for send_button_message()"
#                     }
#                     ]
#                 }
#             }
#         }
#     })
#
#     log("sending button to {recipient}: ".format(recipient=recipient_id))
#
#     call_send_api(message_data)
#
#
# def send_share_message(recipient_id):
#
#     # Share button only works with Generic Template
#     message_data = json.dumps({
#         "recipient": {
#             "id": recipient_id
#         },
#         "message": {
#             "attachment": {
#                 "type":"template",
#                 "payload":{
#                     "template_type":"generic",
#                     "elements":[
#                     {
#                         "title":"Reddit link",
#                         "subtitle":"Something funny or interesting",
#                         "image_url":"https://pbs.twimg.com/profile_images/667516091330002944/wOaS8FKS.png",
#                         "buttons":[
#                         {
#                             "type":"element_share"
#                         }
#                         ]
#                     }
#                     ]
#                 }
#
#             }
#         }
#     })
#
#     log("sending share button to {recipient}: ".format(recipient=recipient_id))
#
#     call_send_api(message_data)
#
#
# def received_postback(event):
#
#     sender_id = event["sender"]["id"]        # the facebook ID of the person sending you the message
#     recipient_id = event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
#
#     # The payload param is a developer-defined field which is set in a postback
#     # button for Structured Messages
#     payload = event["postback"]["payload"]
#
#     log("received postback from {recipient} with payload {payload}".format(recipient=recipient_id, payload=payload))
#
#     if payload == 'Get Started':
#         # Get Started button was pressed
#         send_text_message(sender_id, "Welcome to SoCal Echo Bot! Anything you type will be echoed back to you, except for some keywords.")
#     else:
#         # Notify sender that postback was successful
#         send_text_message(sender_id, "Postback called")


def call_send_api(message_data):

    params = {
        "access_token": access_token
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=message_data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(message):  # simple wrapper for logging to stdout on heroku
    sys.stdout.flush()


# @app.route('/', methods=['POST'])
# def set_greeting_text():
#     # Sets greeting text on welcome screen
#     message_data = json.dumps({
#         "setting_type":"greeting",
#         "greeting":{
#             "text":"Hi {{user_first_name}}, welcome to this bot."
#         }
#     })
#     params = {
#         "access_token": os.environ["PAGE_ACCESS_TOKEN"]
#     }
#     headers = {
#         "Content-Type": "application/json"
#     }
    
#     r = requests.post("https://graph.facebook.com/v2.6/me/thread_settings", params=params, headers=headers, data=message_data)
#     if r.status_code != 200:
#         log("setting greeting text")
#         log(r.status_code)
#         log(r.text)

#     return "ok", 200

    
# @app.route('/', methods=['POST'])
# def set_get_started_button():
#     # Sets get started button on welcome screen
#     message_data = json.dumps({
#         "setting_type":"call_to_actions",
#         "thread_state":"new_thread",
#         "call_to_actions":[
#         {
#             "payload":"Get Started"
#         }
#         ]
#     })
#     params = {
#         "access_token": os.environ["PAGE_ACCESS_TOKEN"]
#     }
#     headers = {
#         "Content-Type": "application/json"
#     }
    
#     r = requests.post("https://graph.facebook.com/v2.6/me/thread_settings", params=params, headers=headers, data=message_data)
#     if r.status_code != 200:
#         log("setting get started button")
#         log(r.status_code)
#         log(r.text)

#     return "ok", 200


@app.route('/privacy', methods=['GET'])
def privacy():
    # needed route if you need to make your bot public
    return "Mục đích của con chatbot này là để giúp các bạn học sinh về các vấn đề tuyến sinh. End."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
