from smtplib import SMTP, SMTPAuthenticationError, SMTPConnectError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from answers import answers
from config import configuration


def admin_email():
    smtp_object = SMTP(configuration['domen'], port=configuration['port'])
    smtp_object.starttls()
    smtp_object.login(user=configuration['bot_mail'], password=configuration['mail_password'])
    message = MIMEMultipart()
    message['From'] = configuration['bot_mail']
    message['To'] = configuration['admin_mail']
    message['Subject'] = answers['mail_error_subject']
    message.attach(MIMEText(answers['warning_mail']))
    smtp_object.sendmail(message['From'], message['To'], message.as_string())
    smtp_object.quit()
