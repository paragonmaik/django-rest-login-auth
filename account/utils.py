"""
Utils module.
"""

import os
from django.core.mail import EmailMessage


class Util:
    """
    Class with helpers methods. 
    ...
    Methods:
        send_email(data):
            Sends out the reset email link.
    """
    @staticmethod
    def send_email(data):
        """
        Sends the email with the reset password link to the user.
        """
        email = EmailMessage(
            subject=data["subject"],
            body=data["body"],
            from_email=os.environ.get("EMAIL_FROM"),
            to=[data["receiver_email"]]
        )
        email.send()
