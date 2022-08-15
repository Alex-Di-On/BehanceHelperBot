from smtplib import SMTP, SMTPAuthenticationError, SMTPConnectError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText





# def admin_message(data: dict) -> requests.models.Response:
#     """Sending message to Admin."""
#     method = '/sendMessage'
#     return requests.post(TelegramAPI.URL + TelegramAPI.TOKEN + method, data=data)




#     try:
            #         smtp_object = SMTP(configuration['system_domen'], port=configuration['port'])
            #         smtp_object.starttls()
            #         smtp_object.login(user=configuration['system_mail'], password=configuration['system_mail_password'])
            #         message = MIMEMultipart()
            #         message['From'] = configuration['system_mail']
            #         message['To'] = configuration['admin_mail']
            #         message['Subject'] = answers['mail_error_subject']
            #         message.attach(MIMEText(answers['warning_mail']))
            #         smtp_object.sendmail(message['From'], message['To'], message.as_string())
            #         smtp_object.quit()
            #     except SMTPAuthenticationError:
            #         admin_message({'chat_id': configuration['admin_id'], 'text': answers['error_auth']})
            #     except SMTPConnectError:
            #         admin_message({'chat_id': configuration['admin_id'], 'text': answers['error_connect']})