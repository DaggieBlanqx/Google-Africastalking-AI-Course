import os
import africastalking
from typing import Dict, Any, List, Optional

# --- Africa's Talking Setup ---
AT_USERNAME = os.getenv("AT_USERNAME")
AT_API_KEY = os.getenv("AT_API_KEY")
AT_SHORTCODE = os.getenv("AT_SHORTCODE")  # Optional: Only needed for 2-way

if not AT_USERNAME or not AT_API_KEY:
    raise EnvironmentError(
        "❌ Missing Africa's Talking credentials (AT_USERNAME / AT_API_KEY)"
    )

# Initialize AT client
africastalking.initialize(AT_USERNAME, AT_API_KEY)
_sms = africastalking.SMS


def send_twoway_sms(
    message: str, recipient: str, shortcode: Optional[str] = AT_SHORTCODE
) -> Dict[str, Any]:
    """
    Send a 2-way SMS using Africa's Talking API.

    Args:
        message (str): The message to send.
        recipient (str): The phone number in international format (+254...).
        shortcode (str, optional): Shortcode to use for 2-way SMS.

    Returns:
        dict: API response from Africa's Talking.

    Raises:
        ValueError: If inputs are invalid.
        Exception: If sending fails.
    """
    if not recipient.startswith("+"):
        raise ValueError(
            f"Invalid recipient format: {recipient}. Must be in +2547... format"
        )

    if not message.strip():
        raise ValueError("Message cannot be empty")

    try:
        response = _sms.send(message, [recipient], shortcode)
        print(f"✅ SMS sent to {recipient}: {message}")
        return response
    except Exception as e:
        print(f"❌ SMS failed to {recipient}: {e}")
        raise


def send_bulk_sms(message: str, recipients: List[str]) -> Dict[str, Any]:
    """
    Send a bulk SMS to multiple recipients.

    Args:
        message (str): The message to send.
        recipients (list): List of phone numbers in international format (+254...).

    Returns:
        dict: API response from Africa's Talking.
    """
    if not recipients:
        raise ValueError("Recipients list cannot be empty")

    try:
        response = _sms.send(message, recipients)
        print(f"📩 Bulk SMS sent to {len(recipients)} recipients")
        return response
    except Exception as e:
        print(f"❌ Bulk SMS failed: {e}")
        raise
