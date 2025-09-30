from flask import Blueprint, jsonify, request

sms_bp = Blueprint("sms", __name__)

@sms_bp.route("/", methods=["GET"])
def get_sms_status():
    return jsonify({"service": "sms", "status": "ready"})

@sms_bp.route("/send", methods=["POST"])
def send_sms():
    data = request.get_json()
    to = data.get("to")
    message = data.get("message")

    if not to or not message:
        return jsonify({"error": "Missing 'to' or 'message'"}), 400

    return jsonify({
        "service": "sms",
        "action": "send",
        "to": to,
        "message": message,
        "status": "sent"
    })
