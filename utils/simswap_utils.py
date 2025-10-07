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
_insights = africastalking.Insights


def check_simswap(phone_number: str) -> Dict[str, Any]:
    """
    Check if a phone number has been involved in a SIM swap using Africa's Talking API.

    Args:
        phone_number (str): The phone number to check in international format (+254...).

    Returns:
        dict: API response from Africa's Talking.
    """

    if not phone_number.startswith("+"):
        raise ValueError(
            f"Invalid phone number format: {phone_number}. Must be in +2547... format"
        )

    try:
        response = _insights.check_sim_swap_state(phone_numbers=[phone_number])
        return response
    except Exception as e:
        raise RuntimeError(f"Failed to check SIM swap state: {str(e)}")
