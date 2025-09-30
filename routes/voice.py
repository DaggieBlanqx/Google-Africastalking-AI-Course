from flask import Blueprint, request, Response

voice_bp = Blueprint("voice", __name__)

# Dummy balance data (replace with DB or service lookup later)
BALANCE_DATA = {
    "+254711XXXYYY": 100,
    "+254733YYYZZZ": 150,
    "+254711000ZZZ": 190,
}


@voice_bp.route("/", methods=["GET"])
def get_voice_status():
    return {"service": "voice", "status": "ready"}


@voice_bp.route("/check-balance", methods=["POST"])
def check_balance():
    """
    Handle voice callback for checking balance.
    Africa's Talking will POST sessionId, isActive, callerNumber, etc.
    """

    session_id = request.values.get("sessionId")
    is_active = request.values.get("isActive")

    if is_active == "1":
        caller_number = request.values.get("callerNumber")

        # Check balance
        if caller_number in BALANCE_DATA:
            balance = BALANCE_DATA[caller_number]
            text = f"Your balance is {balance} shillings. Good bye."
        else:
            text = (
                "Sorry, your phone number is not registered for this service. Good Bye."
            )

        # Build XML response
        response = '<?xml version="1.0" encoding="UTF-8"?>'
        response += "<Response>"
        response += f"<Say>{text}</Say>"
        response += "</Response>"

        return Response(response, mimetype="text/plain")

    else:
        # Call has ended — log details if needed
        duration = request.values.get("durationInSeconds")
        currency = request.values.get("currencyCode")
        amount = request.values.get("amount")

        print(
            f"📞 Call ended. Session: {session_id}, Duration: {duration}s, "
            f"Cost: {amount} {currency}"
        )

        # No response expected when isActive != 1
        return Response("", status=200)


@voice_bp.route("/status", methods=["POST"])
def voice_status():
    """
    Handle Africa's Talking Voice API notifications:
    - Outbound calls
    - Inbound calls
    - After input (GetDigits, Record)
    - When call ends

    AT will send a variety of parameters depending on the event type.
    """

    # Collect all request parameters
    payload = {key: request.values.get(key) for key in request.values.keys()}

    # Log the notification
    print("📢 Voice Notification Received:")
    for key, value in payload.items():
        print(f"   {key}: {value}")

    # Example: Extract a few key fields for easier debugging
    session_id = payload.get("sessionId")
    is_active = payload.get("isActive")
    direction = payload.get("direction")
    caller = payload.get("callerNumber")
    dest = payload.get("destinationNumber")
    hangup_cause = payload.get("hangupCause")

    print(
        f"➡️ Session {session_id} | Active={is_active} | Direction={direction} | "
        f"Caller={caller} | Dest={dest} | HangupCause={hangup_cause}"
    )

    # Always respond with "OK" (200) so AT knows we received it
    return Response("OK", status=200)
