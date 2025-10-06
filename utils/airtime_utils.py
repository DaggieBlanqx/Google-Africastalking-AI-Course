import os
import africastalking
from typing import Dict, Any

# --- Africa's Talking Setup ---
AT_USERNAME = os.getenv("AT_USERNAME")
AT_API_KEY = os.getenv("AT_API_KEY")

if not AT_USERNAME or not AT_API_KEY:
    raise EnvironmentError(
        "❌ Missing Africa's Talking credentials (AT_USERNAME / AT_API_KEY)"
    )

# Initialize AT client
africastalking.initialize(AT_USERNAME, AT_API_KEY)
_airtime = africastalking.Airtime


def send_airtime(
    phone_number: str, amount: float, currency: str = "KES"
) -> Dict[str, Any]:
    """
    Send airtime to a phone number using Africa's Talking API.

    Args:
        phone_number (str): The recipient's phone number in international format (+254...).
        amount (float): The amount of airtime to send.

    Returns:
        dict: API response from Africa's Talking.
    """

    if not phone_number.startswith("+"):
        raise ValueError(
            f"Invalid phone number format: {phone_number}. Must be in +2547... format"
        )

    try:
        response = _airtime.send(phone_number, amount, currency)

        return response
    except Exception as e:
        raise RuntimeError(f"Failed to send airtime: {str(e)}")
