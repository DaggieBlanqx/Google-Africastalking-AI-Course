from flask import Blueprint, request, Response
from utils.voice_utils import make_call

voice_bp = Blueprint("voice", __name__)


@voice_bp.route("/", methods=["GET"])
def get_voice_status():
    return {"service": "voice", "status": "ready"}


@voice_bp.route("/invoke-call", methods=["GET"])
def make_voice_call():
    """
    Get a query parameter 'phone' to make a call to.
    E.g., /invoke-call?phone=2547XXXXXXX
    """

    phone = "+" + request.args.get("phone", "").strip()

    print(f"📞 Request to call: {phone}")
    if not phone:
        return {"error": "Missing 'phone' query parameter"}, 400

    try:
        response = make_call(phone)
        return {"message": f"Call initiated to {phone}", "response": response}
    except Exception as e:
        return {"error": str(e)}, 500


@voice_bp.route("/instruct", methods=["POST"])
def voice_instruct():
    """
    Handle Africa's Talking Voice API call instructions.
    This endpoint is called when a call is answered to get the next set of instructions.
    """

    session_id = request.values.get("sessionId")
    caller_number = request.values.get("callerNumber")
    destination_number = request.values.get("destinationNumber")

    print(
        f"📞 Call answered. Session: {session_id}, Caller: {caller_number}, "
        f"Destination: {destination_number}"
    )

    # Example instructions: Greet the caller and end the call
    response = '<?xml version="1.0" encoding="UTF-8"?>'
    response += "<Response>"
    response += (
        "<Say>Welcome to the service. This is a demo voice application. Goodbye.</Say>"
    )
    response += "</Response>"

    return Response(response, mimetype="text/plain")


@voice_bp.route("/events", methods=["POST"])
def voice_events():
    """
    Handle Africa's Talking Voice API call events.
    This endpoint receives events like call started, ended, failed, etc.
    """

    # Collect all request parameters
    payload = {key: request.values.get(key) for key in request.values.keys()}

    # Log the event
    print("📢 Voice Event Received:")
    for key, value in payload.items():
        print(f"   {key}: {value}")

    # Example: Extract a few key fields for easier debugging
    session_id = payload.get("sessionId")
    event_type = payload.get("eventType")
    caller = payload.get("callerNumber")
    dest = payload.get("destinationNumber")
    hangup_cause = payload.get("hangupCause")

    print(
        f"➡️ Session {session_id} | EventType={event_type} | Caller={caller} | "
        f"Dest={dest} | HangupCause={hangup_cause}"
    )

    # Always respond with "OK" (200) so AT knows we received it
    return Response("OK", status=200)
