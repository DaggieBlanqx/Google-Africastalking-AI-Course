from flask import Blueprint, jsonify, request
import os
import africastalking

sms_bp = Blueprint("sms", __name__)

# --- Africa's Talking Setup ---
AT_API_KEY = os.getenv("AT_API_KEY")
AT_USERNAME = os.getenv("AT_USERNAME") or "sandbox"  # default for dev

africastalking.initialize(AT_USERNAME, AT_API_KEY)
sms = africastalking.SMS


@sms_bp.route("/", methods=["GET"])
def get_sms_status():
    return jsonify({"service": "sms", "status": "ready"})


@sms_bp.route("/twowaycallback", methods=["POST"])
def twoway_callback():
    """
    Handle two-way SMS callbacks from Africa's Talking.
    """
    linkId = request.values.get("linkId")
    text = request.values.get("text")
    to = request.values.get("to")
    msg_id = request.values.get("id")
    date = request.values.get("date")
    sender = request.values.get("from")

    # Respond with a new SMS back to the sender
    send_two_way_sms(
        message=f'This is a response to: "{text}"',
        recipient=sender,
    )

    return "GOOD", 200


def send_two_way_sms(message: str, recipient: str):
    """
    Send a 2-way SMS using Africa's Talking API.
    """
    options = {
        "to": [recipient],
        "message": message,
        "from_": "21477",  # your short code or alphanumeric senderId
    }

    try:
        response = sms.send(options)
        print("✅ SMS sent:", response)
    except Exception as e:
        print("❌ SMS failed:", str(e))
