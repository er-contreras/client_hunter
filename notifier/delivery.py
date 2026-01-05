from notifier.lead import Lead
import requests
import json

class DeliveryChannel:
    def send(self, lead: Lead) -> None:
        raise NotImplementedError("DeliveryChannel.send must be implemented")

class ConsoleDelivery(DeliveryChannel):
    def send(self, lead: Lead) -> None:
        print("\n=== NEW QUALIFIED LEAD ===")
        print(f"Name: {lead.name}")
        print(f"Phone: {lead.phone}")
        print(f"Email: {lead.email}")
        print(f"Source: {lead.source}")
        print("==========================\n")

class WebhookDelivery:
    def __init__(self, url: str):
        self.url = url

    def send(self, lead: Lead):
        payload = {
            "timestamp": lead.timestamp,
            "name": lead.name,
            "phone": lead.phone,
            "email": lead.email,
            "message": lead.message,
            "source": lead.source,
        }
        try:
            resp = requests.post(self.url, json=payload, timeout=5)
            resp.raise_for_status()
            print(f"Webhook sent for {lead.name} ({lead.phone})")
        except Exception as e:
            print(f"Webhook failed for {lead.name}: {e}")

class WhatsAppDelivery:
    """
    Sends a Lead to WhatsApp via the official WhatsApp Cloud API.
    """

    def __init__(self, phone_number_id: str, access_token: str, template_name: str, template_language: str = "en_US"):
        self.url = f"https://graph.facebook.com/v22.0/{phone_number_id}/messages"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        self.template_name = template_name
        self.template_language = template_language

    def send(self, lead: Lead):
        # Ensure phone number is in international format without "+"
        to_phone = "".join(filter(str.isdigit, lead.phone))

        payload = {
            "messaging_product": "whatsapp",
            "to": to_phone,
            "type": "template",
            "template": {
                "name": self.template_name,
                "language": {"code": self.template_language},
                # Optional: You can include template parameters here
                # "components": [{"type": "body", "parameters": [{"type": "text", "text": lead.name}]}]
            }
        }

        try:
            resp = requests.post(self.url, headers=self.headers, json=payload, timeout=5)
            resp.raise_for_status()
            print(f"WhatsApp sent to {lead.phone} ({lead.name})")
        except Exception as e:
            print(f"WhatsApp delivery failed for {lead.phone}: {e}")
            if resp is not None:
                print(f"Response: {resp.text}")
