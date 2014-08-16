from smtplib import SMTP_SSL
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.mime.text import MIMEText
from email import Encoders
import base64

address_to = "admin@yourdomain.com"
address_from = 'sitepinger@yourdomain.com'
address_from_psw = 'password'

def sendmsg(title, message):
	# Compose message
	msg = MIMEMultipart('alternative')
	msg['Subject'] = title
	msg['From'] = address_from
	msg['To'] = address_to
	msg.attach(MIMEText(message, 'html'))

	# Send mail
	smtp = SMTP_SSL()
	smtp.connect('smtp.mailserver.com')
	smtp.login(address_from, address_from_psw)
	smtp.sendmail(address_from, address_to, msg.as_string())
	smtp.quit()
