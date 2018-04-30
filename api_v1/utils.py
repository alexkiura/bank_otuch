import sendgrid
from sendgrid.helpers.mail import Email, Mail, Content
from django.conf import settings


def send_mail(content, email_from, email_to, subject):
    send_client = sendgrid.SendGridAPIClient(
        apikey=settings.SENDGRID_API_KEY
    )
    from_email = Email(email_from)
    to_email = Email(email_to)
    subject = subject
    content = Content("text/plain", content)
    mail = Mail(from_email, subject, to_email, content)
    response = send_client.client.mail.send.post(request_body=mail.get())
    return response
