import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

message_object = MIMEMultipart()
text_message = 'Hi'

message_object['From'], message_object['To'], message_object['Subject'] = 'admin@alex-di.com', 'alexditarget@gmail.com', 'Topic'

message_object.attach(MIMEText(text_message))

port = 587

smtp_object = smtplib.SMTP('alex-di.com', port=port)

smtp_object.starttls()

smtp_object.login(user=message_object['From'], password='aQ4jI4yG5n')

smtp_object.sendmail(message_object['From'], message_object['To'], message_object.as_string())

# Прописать в terminate
smtp_object.quit()
