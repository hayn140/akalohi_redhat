import os
import json
import datetime

def lambda_handler(event, context):
    # expected header name (case-insensitive)
    secret_header = None
    headers = event.get("headers") or {}
    for k, v in headers.items():
        if k.lower() == "x-webhook-secret":
            secret_header = v
            break

    expected = os.environ.get("WEBHOOK_SECRET")
    if expected is None:
        print("ERROR: WEBHOOK_SECRET not set in environment")  # log misconfig
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Server misconfiguration: secret not set"}),
        }

    if secret_header != expected:
        print(f"Forbidden attempt: provided secret='{secret_header}' expected='{expected}'")  # log invalid
        return {
            "statusCode": 403,
            "body": json.dumps({"error": "Forbidden: invalid secret"}),
        }

    # Successful invocation
    print("The webhook worked", {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "received_body": event.get("body"),
        "request_id": context.aws_request_id,
    })

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Webhook received and validated",
            "input_event": event.get("body"),
        }),
    }
