from notifier.lead import Lead
from email.message import EmailMessage
from notifier.logger import log_delivery
import smtplib

class EmailDelivery:
    def __init__(
        self,
        smtp_host="localhost",
        smtp_port=1025,
        from_addr="leads@clienthunter.local",
        username=None,
        password=None,
        use_tls=False,
    ):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.from_addr = from_addr
        self.username  = username
        self.password  = password
        self.use_tls   = use_tls

    def send(self, lead: Lead):
        if not lead.email:
            print("No email provided - skipping email delivery")
            log_delivery("email", lead, "SKIPPED", "no-email")
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

        try:
            server = smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=10)
            
            if self.use_tls:
                server.starttls()

            if self.username and self.password:
                server.login(self.username, self.password)


            server.send_message(msg)
            server.quit()

            print(f"Email sent to {lead.email}")
            log_delivery("email", lead, "SENT", self.smtp_host)

        except Exception as e:
            print(f"Email delivery failed: {e}")
            log_delivery("email", lead, "FAILED", str(e))
