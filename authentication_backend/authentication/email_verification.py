from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings


def send_email_verification(user, site_url, otp):
    confirmation_token = default_token_generator.make_token(user)  # unique token
    activation_link = f"{site_url}/users/api/users/activate/{user.id}/{confirmation_token}"  # activation link to be sent in email

    send_mail(
        subject="Confirm Account Creation Details",
        message= (
            "You're receiving this email because you need to finish the activation process. \n \n"
            f"Here's your OTP {otp} \n \n"
            "or \n \n"
            "Please go to the following page to activate account: \n"
            f"{activation_link} \n \n"
            "Thanks for using our site! \n \n"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False, # Raises an smtplib.SMTPException if an error occurs
    )