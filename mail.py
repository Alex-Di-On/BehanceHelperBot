import sys
from smtplib import SMTP, SMTPAuthenticationError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sys import exit

from config import configuration


message = MIMEMultipart()
error_mail = 'Warning! There is a problem with DataBase connection for BehanceHelperBot. Check functionality of DataBase on REG.RU, please.'
message['From'] = 'admin@alex-di.com'
message['To'] = 'alexditarget@gmail.com'
message['Subject'] = 'Warning! DataBase connection error!'
message.attach(MIMEText(error_mail))

port = 587

# try:
#     smtp_object = SMTP('alex-di.com', port=port)
#     smtp_object.starttls()
#     smtp_object.login(user=message['From'], password='aQ4jI4yG5n')
# except SMTPAuthenticationError:
#     sys.exit('Сорри!')

smtp_object.sendmail(message['From'], message['To'], message.as_string())
# Прописать в terminate
smtp_object.quit()
