from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import configuration


def admin_email() -> None:
    """Sending warning email to Admin."""
    smtp_object = SMTP(configuration['domen'], port=configuration['port'])
    smtp_object.starttls()
    smtp_object.login(user=configuration['bot_mail'], password=configuration['mail_password'])
    message = MIMEMultipart()
    message['From'] = configuration['bot_mail']
    message['To'] = configuration['admin_mail']
    message['Subject'] = 'Warning! DataBase connection error!'
    message.attach(MIMEText('Warning! There is a problem with DataBase connection for BehanceHelperBot. '
                            'Check functionality of DataBase on REG.RU, please.'))
    smtp_object.sendmail(message['From'], message['To'], message.as_string())
    smtp_object.quit()


def language_test(word: str) -> bool:
    """Checking that message is written in English."""
    for i in list(word):
        if ord(i) not in range(32, 128):
            return False
    return True


buttons_menu = [
    ["Author's project views"],
    ["Author's appreciations"],
    ["Author's followers"],
    ["Author's following"],
    ["Author's country"],
    ['REQUEST HISTORY'],
    ['CHANGE URL']
]


bot_answers = {
    'nobody_texted': "No one texted to bot!",
    'start': "Please, input author's URL on Behance:",
    'menu': 'What info would you like to receive?',
    'no_portfolio': "Author hasn't portfolio on Behance.",
    'language_test': "I don't understand you. Use English, please.",
    'error_db': "Sorry, I can't answer you at the moment. Please, try again later.",
    'empty_history': 'Your request history is empty.',
    'no_history': "Sorry, I don't see your request history. Please, input author's URL on Behance again."
}
