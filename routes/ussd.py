from flask import Blueprint, request, Response

ussd_bp = Blueprint("ussd", __name__)


@ussd_bp.route("/", methods=["GET"])
def index():
    return "Welcome to the USSD service"


@ussd_bp.route("/session", methods=["POST"])
def ussd_handler():
    # Read the variables sent via POST from our API
    session_id = request.values.get("sessionId", None)
    serviceCode = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "")

    # Print the details
    print(f"session_id: {session_id}")
    print(f"serviceCode: {serviceCode}")

    if text == "":
        # First request. Start response with CON
        response = "CON What would you want to check \n"
        response += "1. My Account \n"
        response += "2. My phone number"

    elif text == "1":
        # First level response
        response = "CON Choose account information you want to view \n"
        response += "1. Account number"

    elif text == "2":
        # Terminal request
        response = "END Your phone number is " + str(phone_number)

    elif text == "1*1":
        # Second level response
        accountNumber = "ACC1001"
        response = "END Your account number is " + accountNumber

    else:
        response = "END Invalid choice"

    return response


ussd_bp.route("/status", methods=["POST"])


def ussd_status():
    """
    Handle USSD end-of-session notifications.
    Expected payload (form-data):
    {
      "date": "2025-09-29 12:00:00",
      "sessionId": "...",
      "serviceCode": "*123#",
      "networkCode": "63902",
      "phoneNumber": "+254711000111",
      "status": "Success",
      "cost": "KES 0.10",
      "durationInMillis": "12345",
      "hopsCount": "3",
      "input": "1*1",
      "lastAppResponse": "END Your account number is ACC1001",
      "errorMessage": "..." (optional)
    }
    """
    payload = {key: request.values.get(key) for key in request.values.keys()}

    print("📲 USSD Status Notification Received:")
    for key, value in payload.items():
        print(f"   {key}: {value}")

    # Always acknowledge with 200 OK
    return Response("OK", status=200)
