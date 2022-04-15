from django.core.mail import send_mail


def send_confirmation_code(confirmation_code, email):
    send_mail(
        subject='Confirmation code',
        message=f'Your confirmation code {confirmation_code}',
        from_email='confirmationcode@mail.ru',
        recipient_list=[email]
    )
