from flask import Blueprint, jsonify, request, Response
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

    if not linkId or not text or not to or not msg_id or not date or not sender:
        return "BAD", 400
    print(f"Received 2-way SMS from {sender}: {text}")

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


@sms_bp.route("/delivery-reports", methods=["POST"])
def sms_delivery_report():
    """
    Handle SMS delivery reports.
    Expected form-data payload:
    {
      "id": "...",
      "status": "...",
      "phoneNumber": "...",
      "networkCode": "...",
      "failureReason": "...",
      "retryCount": "..."
    }
    """
    payload = {key: request.values.get(key) for key in request.values.keys()}

    print("📩 SMS Delivery Report Received:")
    for key, value in payload.items():
        print(f"   {key}: {value}")

    return Response("OK", status=200)


@sms_bp.route("/opt-out", methods=["POST"])
def sms_opt_out():
    """
    Handle Bulk SMS Opt-Out notifications.
    Expected form-data payload:
    {
      "senderId": "MyBrand",
      "phoneNumber": "+254711XXXYYY"
    }
    """
    payload = {key: request.values.get(key) for key in request.values.keys()}

    print("🚫 SMS Opt-Out Notification Received:")
    for key, value in payload.items():
        print(f"   {key}: {value}")

    return Response("OK", status=200)


@sms_bp.route("/subscription", methods=["POST"])
def sms_subscription():
    """
    Handle Premium SMS subscription notifications.
    Expected form-data payload:
    {
      "phoneNumber": "+254711000111",
      "shortCode": "12345",
      "keyword": "NEWS",
      "updateType": "addition" // or "deletion"
    }
    """
    payload = {key: request.values.get(key) for key in request.values.keys()}

    print("⭐ SMS Subscription Notification Received:")
    for key, value in payload.items():
        print(f"   {key}: {value}")

    # Example: Extract values
    phone_number = payload.get("phoneNumber")
    short_code = payload.get("shortCode")
    keyword = payload.get("keyword")
    update_type = payload.get("updateType")

    print(
        f"➡️ Subscription update for {phone_number}: "
        f"{update_type.upper()} to '{keyword}' on shortcode {short_code}"
    )

    return Response("OK", status=200)
