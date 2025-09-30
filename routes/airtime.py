from flask import Blueprint, request, jsonify

airtime_bp = Blueprint("airtime", __name__)


@airtime_bp.route("/", methods=["GET"])
def get_airtime_status():
    return jsonify({"service": "airtime", "status": "ready"})


@airtime_bp.route("/validation", methods=["POST"])
def airtime_validation():
    """
    Validate an airtime transaction request.
    Expected payload:
    {
        "transactionId": "SomeTransactionID",
        "phoneNumber": "+254711XXXYYY",
        "sourceIpAddress": "127.12.32.24",
        "currencyCode": "KES",
        "amount": 500.00
    }
    """
    data = request.get_json(force=True)

    transaction_id = data.get("transactionId")
    phone_number = data.get("phoneNumber")
    source_ip = data.get("sourceIpAddress")
    currency = data.get("currencyCode")
    amount = data.get("amount")

    # Basic validation logic (you can replace with real checks)
    if transaction_id and phone_number and currency and amount and source_ip:
        status = "Validated"
    else:
        status = "Failed"

    return jsonify({"status": status})


@airtime_bp.route("/status", methods=["POST"])
def airtime_status():
    """
    Handle airtime delivery status callbacks.
    Expected payload:
    {
       "phoneNumber":"+254711XXXYYY",
       "description":"Airtime Delivered Successfully",
       "status":"Success",
       "requestId":"ATQid_SampleTxnId123",
       "discount":"KES 0.6000",
       "value":"KES 100.0000"
    }
    """
    data = request.get_json(force=True)

    phone_number = data.get("phoneNumber")
    description = data.get("description")
    status = data.get("status")
    request_id = data.get("requestId")
    discount = data.get("discount")
    value = data.get("value")

    if not phone_number or not status or not request_id and not discount and not value:
        return "BAD", 400

    # Log or process the status here
    print(f"📲 Airtime status update for {phone_number}: {status} ({description})")

    # Respond with 200 OK and body "OK"
    return "OK", 200
