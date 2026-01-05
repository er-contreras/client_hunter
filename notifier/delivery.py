from notifier.lead import Lead

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
