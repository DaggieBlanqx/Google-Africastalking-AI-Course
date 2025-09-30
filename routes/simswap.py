from flask import Blueprint, request

simswap_bp = Blueprint("sim-swap", __name__)


@simswap_bp.route("/", methods=["GET"])
def get_simswap_status():
    return {"service": "sim-swap", "status": "ready"}


@simswap_bp.route("/status", methods=["POST"])
def simswap_status():
    """
    Handle SIM swap status callbacks.
    Expected payload:
    {
      "status": "Swapped",
      "lastSimSwapDate": "01-01-1900",
      "providerRefId": "fe3b-46fd-931c-b2ef3a64da93311064104",
      "requestId": "ATSwpid_4032b7bfddd5fdca0c401184a84cbb0d",
      "transactionId": "738e202b-ea2f-43e5-b451-a85334e90fb5"
    }
    """
    data = request.get_json(force=True)

    status = data.get("status")
    last_sim_swap_date = data.get("lastSimSwapDate")
    provider_ref_id = data.get("providerRefId")
    request_id = data.get("requestId")
    transaction_id = data.get("transactionId")

    # Log or process the status update
    print(
        f"📲 SIM swap status update: {status}, "
        f"last swap: {last_sim_swap_date}, "
        f"providerRefId: {provider_ref_id}, "
        f"requestId: {request_id}, "
        f"transactionId: {transaction_id}"
    )

    # Respond with 200 OK and body "OK"
    return "OK", 200
