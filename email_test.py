import imaplib
import email
from email.header import decode_header
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

# EmailParser class (reused from previous code)
class EmailParser:
    def __init__(self, config_path="config.json"):
        self.config = self.load_config(config_path)
    
    def load_config(self, config_path):
        try:
            with open(config_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "username": " ",  # Replace with your email
                "password": " ",  # Replace with your app password
                "sales_channel_email": " ",  # Communication channel email
                "log_file": "email_parser.log"
            }

    def send_email(self, to_address, subject, body):
        """Function to send email to a specified address."""
        msg = MIMEMultipart()
        msg['From'] = self.config["username"]
        msg['To'] = to_address
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        try:
            server = smtplib.SMTP(self.config["smtp_server"], self.config["smtp_port"])
            server.starttls()
            server.login(self.config["username"], self.config["password"])
            server.send_message(msg)
            server.quit()
            print(f"Email forwarded to {to_address}")
        except Exception as e:
            print(f"Error sending email: {e}")

# Function to fetch unread emails from the inbox (checking specific sender and recipient)
def fetch_emails():
    # Email credentials for your email account (for testing)
    username = " "  # Replace with the email you want to check (harsh@ccdocs.com)
    password = " "  # Use app password if 2FA is enabled

    # Connect to the Gmail IMAP server
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(username, password)
    mail.select("inbox")  # Default is INBOX

    # Search for unread emails (UNSEEN) from 'your@gmail.com' to 'yoursreply@gmail.com'
    status, messages = mail.search(None, '(UNSEEN FROM " " TO " ")')
    
    # If there are any new emails
    if status == "OK":
        for msg_id in messages[0].split():
            # Fetch the email by ID
            status, msg_data = mail.fetch(msg_id, "(RFC822)")
            if status == "OK":
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding if encoding else "utf-8")
                        
                        # Get the email body
                        body = ""
                        if msg.is_multipart():
                            for part in msg.walk():
                                if part.get_content_type() == "text/plain":
                                    body = part.get_payload(decode=True).decode()
                                    break
                        else:
                            body = msg.get_payload(decode=True).decode()
                        
                        # Now process the email and forward it to the communication channel
                        email_parser = EmailParser()
                        email_parser.send_email(email_parser.config["sales_channel_email"], subject, body)
    
    # Logout after processing
    mail.logout()

# Run the function to fetch and forward emails
fetch_emails()
