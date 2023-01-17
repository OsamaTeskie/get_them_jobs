from twilio.rest import Client
import os


account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

def sendMessage(messageBody):
    client.messages.create(
        body=messageBody,
        from_='whatsapp:+14155238886',
        to='whatsapp:+16475331335'
    )