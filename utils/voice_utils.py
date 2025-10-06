import os
import africastalking
from typing import Dict, Any, Optional

# --- Africa's Talking Setup ---
AT_USERNAME = os.getenv("AT_USERNAME")
AT_API_KEY = os.getenv("AT_API_KEY")
AT_VOICE_NUMBER = os.getenv("AT_VOICE_NUMBER")

if not AT_USERNAME or not AT_API_KEY or not AT_VOICE_NUMBER:
    raise EnvironmentError(
        "❌ Missing Africa's Talking credentials (AT_USERNAME / AT_API_KEY / AT_VOICE_NUMBER)"
    )

# Initialize AT client
africastalking.initialize(AT_USERNAME, AT_API_KEY)
_voice = africastalking.Voice


def make_call(
    phone_number: str, from_number: Optional[str] = AT_VOICE_NUMBER
) -> Dict[str, Any]:
    """
    Make a voice call using Africa's Talking API.

    Args:
        phone_number (str): The phone number to call in international format (+254...).
        from_number (str, optional): The caller ID or shortcode to use.

    Returns:
        dict: API response from Africa's Talking.
    """

    if not phone_number.startswith("+"):
        raise ValueError(
            f"Invalid phone number format: {phone_number}. Must be in +2547... format"
        )

    try:
        response = _voice.call(callTo=[phone_number], callFrom=from_number)
        print(f"📞 Call initiated to {phone_number}")
        return response
    except Exception as e:
        print(f"❌ Call failed to {phone_number}: {e}")
        raise
