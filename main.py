import bitly_api
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import emailpass


def shorten():
    with open("accessToken.txt") as f:
        token = f.readlines()

    BITLY_ACCESS_TOKEN = token

    b = bitly_api.Connection(access_token=BITLY_ACCESS_TOKEN)

    a = input("Please enter the url to shorten: ")
    
    # Bitly requires out url to be following https protocol so if our url is not in https, it will add the https protocol
    if(a[:8] != 'https://'):
        a = 'https://' + a     
    
    response = b.shorten(a)
    return response["url"]


def sending_email():
    
    returned_url = shorten();
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    EMAIL = emailpass.EMAIL
    PASSWORD = emailpass.PASSWORD

    server.login(EMAIL, PASSWORD)

    from_addr = 'sender email address'
    to_addr = ['receiver email address']

    message = MIMEMultipart()
    message["From"] = from_addr
    message["To"] = " ,".join(to_addr)
    message["Subject"] = "The Shortened URL"
    body = "Your shortened URL is: " + returned_url

    message.attach(MIMEText(body, 'plain'))
    text = message.as_string()

    server.sendmail(from_addr, to_addr, text)
    print("Mail Sent Successfully")
    server.quit()

if __name__ == "__main__":
    sending_email()

# run program using ->
#                        python -W ignore main.py
# because there are some syntax warning in bitly_api.py file in bitly_api module.
