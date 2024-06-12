import threading
from django.core.mail import EmailMessage

from_email = 'gift200161@gmail.com'


class EmailThread(threading.Thread):
    def __init__(self, email):
        super().__init__()
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=True)


def send_alert_email(subject, message):
    to_email = ['giftmugaragumbojr@gmail.com']
    email = EmailMessage(
        subject=subject,
        body=message,
        to=to_email,
        from_email=from_email
    )
    EmailThread(email).start()


def send_guess_pass_email():
    subject = "Alert: Password Guess Detected!"
    message = """
    Alert: Password Guess Detected!

    A Password Guess attempt has been detected in the network logs.

    Please investigate this incident promptly.
    """
    send_alert_email(subject, message)


def send_smurf_email():
    subject = "Alert: Smurf Attack Detected!"
    message = """
    Alert: Smurf Attack Detected!

    A Smurf attack has been detected in the network logs.

    Please investigate this incident promptly.
    """
    send_alert_email(subject, message)


def send_spy_email():
    subject = "Alert: Spy Activity Detected!"
    message = """
    Alert: Spy Activity Detected!

    Spy activity has been detected in the network logs.

    Please investigate this incident promptly.
    """
    send_alert_email(subject, message)


def send_ipsweep_email():
    subject = "Alert: IP Sweep Detected!"
    message = """
    Alert: IP Sweep Detected!

    An IP Sweep has been detected in the network logs.

    Please investigate this incident promptly.
    """
    send_alert_email(subject, message)


def send_neptune_email():
    subject = "Alert: Neptune Attack Detected!"
    message = """
    Alert: Neptune Attack Detected!

    A Neptune attack has been detected in the network logs.

    Please investigate this incident promptly.
    """
    send_alert_email(subject, message)


def send_teardrop_email():
    subject = "Alert: Teardrop Attack Detected!"
    message = """
    Alert: Teardrop Attack Detected!

    A Teardrop attack has been detected in the network logs.

    Please investigate this incident promptly.
    """
    send_alert_email(subject, message)


def send_satan_email():
    subject = "Alert: Satan Attack Detected!"
    message = """
    Alert: Satan Attack Detected!

    A Satan attack has been detected in the network logs.

    Please investigate this incident promptly.
    """
    send_alert_email(subject, message)
