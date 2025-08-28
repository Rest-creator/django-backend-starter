# core/gateways/stripe_gateway.py
class StripeGateway:
    def charge(self, amount: float, currency: str, source: str) -> dict:
        """
        Call Stripe API to charge the card.
        Return dict with { "success": True/False, "transaction_ref": "xxxx" }
        """
        # Stripe API integration here
        return {"success": True, "transaction_ref": "stripe_tx_123"}
