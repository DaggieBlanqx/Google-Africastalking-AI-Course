from flask import Blueprint, jsonify, request, Response
from utils.sms_utils import send_bulk_sms, send_twoway_sms


sms_bp = Blueprint("sms", __name__)


@sms_bp.route("/", methods=["GET"])
def get_sms_status():
    return jsonify({"service": "sms", "status": "ready"})


@sms_bp.route("/invoke-bulk-sms", methods=["GET"])
def invoke_bulk_sms():
    """
    Get a query parameter 'phone' and 'message' to send an SMS to.
    E.g., /invoke-bulk-sms?phone=2547XXXXXXX&message=Hello%20World
    """

    phone = "+" + request.args.get("phone", "").strip()
    message = request.args.get("message", "Hello from Africa's Talking!").strip()

    print(f"📩 Request to send SMS to: {phone} with message: {message}")
    if not phone:
        return {"error": "Missing 'phone' query parameter"}, 400

    try:
        response = send_bulk_sms(message, [phone])
        return {"message": f"SMS sent to {phone}", "response": response}
    except Exception as e:
        return {"error": str(e)}, 500


@sms_bp.route("/invoke-twoway-sms", methods=["GET"])
def invoke_twoway_sms():
    """
    Get a query parameter 'phone' and 'message' to send an SMS to.
    E.g., /invoke-twoway-sms?phone=2547XXXXXXX&message=Hello%20World
    """

    phone = "+" + request.args.get("phone", "").strip()
    message = request.args.get("message", "Hello from Africa's Talking!").strip()

    print(f"📩 Request to send SMS to: {phone} with message: {message}")
    if not phone:
        return {"error": "Missing 'phone' query parameter"}, 400

    try:
        response = send_twoway_sms(message, phone)
        return {"message": f"SMS sent to {phone}", "response": response}
    except Exception as e:
        return {"error": str(e)}, 500


@sms_bp.route("/twoway", methods=["POST"])
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
    send_twoway_sms(
        message=f'This is a response to: "{text}"',
        recipient=sender,
    )

    return "GOOD", 200


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
