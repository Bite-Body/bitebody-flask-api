import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

port = 465  # For SSL

smtp_server = "smtp.gmail.com"
sender = "bitebodyxyztest@gmail.com"
getter = "bitebodyxyz@gmail.com"
password = "tester_account404"


message = MIMEMultipart("alternative")
message["subject"] = "Bitebody.xyz Account Password Recovery"
message["From"] = sender
message["To"] = getter



# Create the plain-text and HTML version of your message
# text = """\
# Hi,
# How are you?
# Real Python has many great tutorials:
# www.realpython.com"""
html = """\
<html>
  <body>
    <p>According to your recent account activity, you are in need of a replacement password.<br>
       <a href="http://www.realpython.com">CLICK RIGHT HERE</a> 
       to reset your account's password.
    </p>
  </body>
</html>
"""

# Turn these into plain/html MIMEText objects
#part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")

# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
#message.attach(part1)
message.attach(part2)


# Create a secure SSL context
context = ssl.create_default_context()


with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender, password)
    server.sendmail(sender,getter,message.as_string())
    # TODO: Send email here