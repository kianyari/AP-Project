import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailSender():

    __smtp_server = "smtp.gmail.com"
    __smtp_port = 587
    __sender_email = "alosbahoosh@gmail.com"
    __password = "vsmwyaazpqmtrsrc"

    @classmethod
    def send_email(cls, receiver_email, message, subject="Password Recover"):
        # Create a multipart message
        msg = MIMEMultipart()
        msg["From"] = cls.__sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject

        # Add message body
        msg.attach(MIMEText(message, "plain"))

        try:
            with smtplib.SMTP(cls.__smtp_server, cls.__smtp_port) as server:
                server.starttls()
                server.login(cls.__sender_email, cls.__password)
                server.send_message(msg)

            print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email. Error: {str(e)}")


# receiver_email = "kianyarii1383@gmail.com" # -> user bayad bede
# subject = "Password Recover"
# message = f"This is your forgotten password:  <{message}>"  # -> user bayad bede


# EmailSender.send_email(receiver_email, message) # -> karbar bayad runesh kone
