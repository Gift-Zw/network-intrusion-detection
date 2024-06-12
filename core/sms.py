import threading
from twilio.rest import Client

# Twilio configuration
account_sid = 'ACb555accbe14a6470e75cb1af19775def'
auth_token = '8fb67278e8f12a0c9afaabcf3ff61834'
from_phone_number = '+15206140036'

client = Client(account_sid, auth_token)

to_phone_number = '+263776149765'


class SMSThread(threading.Thread):
    def __init__(self, message):
        super().__init__()
        self.to_phone_number = to_phone_number
        self.message = message
        threading.Thread.__init__(self)

    def run(self):
        client.messages.create(
            body=self.message,
            from_=from_phone_number,
            to=self.to_phone_number
        )


def send_alert_sms(message):
    SMSThread(message).start()


def send_guess_pass_sms():
    message = """
    Alert: Password Guess Detected!

    A Password Guess attempt has been detected in the network logs.

    Please investigate this incident promptly.
    """
    send_alert_sms(message)


def send_smurf_sms():
    message = """
    Alert: Smurf Attack Detected!

    A Smurf attack has been detected in the network logs.

    Please investigate this incident promptly.
    """
    send_alert_sms(message)


def send_spy_sms():
    message = """
    Alert: Spy Activity Detected!

    Spy activity has been detected in the network logs.

    Please investigate this incident promptly.
    """
    send_alert_sms(message)


def send_ipsweep_sms():
    message = """
    Alert: IP Sweep Detected!

    An IP Sweep has been detected in the network logs.

    Please investigate this incident promptly.
    """
    send_alert_sms(message)


def send_neptune_sms():
    message = """
    Alert: Neptune Attack Detected!

    A Neptune attack has been detected in the network logs.

    Please investigate this incident promptly.
    """
    send_alert_sms(message)


def send_teardrop_sms():
    message = """
    Alert: Teardrop Attack Detected!

    A Teardrop attack has been detected in the network logs.

    Please investigate this incident promptly.
    """
    send_alert_sms(message)


def send_satan_sms():
    message = """
    Alert: Satan Attack Detected!

    A Satan attack has been detected in the network logs.

    Please investigate this incident promptly.
    """
    send_alert_sms(message)
