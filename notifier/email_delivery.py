from notifier.lead import Lead
from email.message import EmailMessage
import smtplib

class EmailDelivery:
    def __init__(self, smtp_host="localhost", smtp_port=1025, from_addr="leads@clienthunter.local"):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.from_addr = from_addr

    def send(self, lead: Lead):
        if not lead.email:
            print("No email provided - skipping email delivery")
            return

        msg = EmailMessage()
        msg["From"] = self.from_addr
        msg["To"] = lead.email
        msg["Subject"] = "Quick question about your business"

        msg.set_content(
            f"""
            Hi {lead.name},

            I came across your business and noticed a few areas where technology could
            help you get more clients or save time.

            If you're open to it, I'd be happy to share a quick idea, no commitment.

            Best,

            Erick
            """
        )

        with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
            server.send_message(msg)

        print(f"Email sent to {lead.email}")
