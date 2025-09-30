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
