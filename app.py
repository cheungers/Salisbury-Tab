import random
from flask import Flask, render_template, request
from pymessenger.bot import Bot

app = Flask(__name__)
ACCESS_TOKEN = "EAAEKDVURsx4BABorA6QazWcsUD2OnHRJsb32eHgUtMMZAr6xUNKwJsGIBIz1rUsCWRA3z24uysmLMyU2ZAF91nanLZBo9ckZCBXzUHHcHQ9ypsGxLDKaB0hK6kyTpl7ZBExj5NvWfNr9uoZCnf99yynkMcDzpq7ADFPiMtO1hmzQZDZD"
VERIFY_TOKEN = 'macca_is_gross'
bot = Bot(ACCESS_TOKEN)
app.debug = True

@app.route('/', methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    else:
        #obtain user's message
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    #Messenger ID of user
                    recipient_id = message['sender']['id']
                    if message['message'].get('text'):
                        response_sent_text = get_message()
                        send_message(recipient_id, response_sent_text)
                    #non-text (GIF, photo, video) message
                    if message['message'].get('attachments'):
                        response_sent_nontext = get_message()
                        send_message(recipient_id, response_sent_nontext)
    return "Message Processed"

def verify_fb_token(token_sent):
    #checks facebook's token against the token you sent. Match = allows request
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def get_message():
    response_messages = ["test", "working", "Salisbury"]
    return random.choice(response_messages)

def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == '__main__':
    app.run()
