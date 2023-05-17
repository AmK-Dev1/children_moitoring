import smtplib
from email.mime.text import MIMEText


class EmailSender:

    def __init__(self):
        """
        """
        self.email = "children_monitoring@outlook.com"
        self.password = "Chmt2023"
        self.smtpServer='smtp.office365.com'
        self.smtpPort = 587
        self.message = "" 
        # Établir une connexion SMTP sécurisée avec le serveur Outlook
        self.smtp_obj = smtplib.SMTP(self.smtpServer, self.smtpPort)
        self.smtp_obj.starttls()
        self.smtp_obj.login(self.email, self.password)

    def logout(self):
        self.smtp_obj.quit()

    def send_email(self,recipient_email,subject,content):
        self.message = MIMEText(content)
        self.message['From'] = self.email
        self.message['To'] = recipient_email
        self.message['Subject'] = subject
        self.smtp_obj.send_message(self.message)
        
        print('email envoyé avec succès')

