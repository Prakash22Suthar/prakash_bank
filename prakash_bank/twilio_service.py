from twilio.rest import Client
from django.conf import settings

class MessageServices:
    def __init__(self):
        self.client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        print('➡ prakash_bank/twilio_service.py:7 self.client:', self.client)
        self.twilio_phone_number = settings.TWILIO_PHONE_NUMBER
        print('➡ prakash_bank/twilio_service.py:9 self.twilio_phone_number:', self.twilio_phone_number)

    def send_sms(self, to_number, message):
        message = self.client.messages.create(
            body=message,
            from_=self.twilio_phone_number,
            to=to_number
        )
        return message

    def make_call(self, to_number, from_number, url):
        call = self.client.calls.create(
            to=to_number,
            from_=from_number,
            url=url
        )
        return call
