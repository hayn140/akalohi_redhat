import os
import json
import boto3
import requests
import hmac
import base64

from botocore.exceptions import ClientError

def get_secret():
    secret_name = "aap_api_key"
    region_name = "us-east-2"

    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        print(f"Error retrieving secret: {e}")
        raise e

    return get_secret_value_response['SecretString']

def lambda_handler(event, context):
    # --- Webhook secret validation ---

    secret_header = None
    headers = event.get("headers") or {}
    for k, v in headers.items():
        if k.lower() == "x-webhook-secret":
            secret_header = v
            break

    expected = os.environ.get("WEBHOOK_SECRET")
    if expected is None:
        print("ERROR: WEBHOOK_SECRET not set in environment")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Server misconfiguration: secret not set"}),
        }

    import hmac
    if not hmac.compare_digest(secret_header or "", expected):
        print(f"Forbidden attempt: provided secret='{secret_header}' expected='***'")
        return {
            "statusCode": 403,
            "body": json.dumps({"error": "Forbidden: invalid secret"}),
        }

    # --- Extract filename from webhook payload ---
    try:
        body_str = event.get("body") or "{}"
        payload = json.loads(body_str)
        filename = payload.get("filename")
        if not filename:
            raise ValueError("Missing 'filename' in webhook payload")
    except Exception as e:
        print(f"Bad payload or missing filename: {e}")
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Bad request: missing or invalid filename"}),
        }

    # --- Trigger AAP Job ---

    api_secret = get_secret()

    print(f"Triggering AAP job for file: {filename}")

    # Parse file extension for image_type
    _, ext = os.path.splitext(filename)
    image_type = ext.lstrip('.').lower()

    # Get temporary AWS credentials (optional - depending if AAP needs them)
    credentials = boto3.Session().get_credentials().get_frozen_credentials()
    aws_access_key = credentials.access_key
    aws_secret_key = credentials.secret_key
    aws_session_token = credentials.token

    # AAP API endpoint and job template ID (adjust as needed)
    job_template_id = 12
    aap_url = f"https://aap-aap.apps.cluster-7zlft-1.dynamic.redhatworkshops.io/api/controller/v2/job_templates/{ job_template_id }/launch/"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_secret}"
    }

    payload = {
        "extra_vars": {
            "s3_key": filename,
            "s3_bucket_name": "akalohi-aws-bucket-imports",   # since no actual bucket here, or remove this if irrelevant
            "aws_region": "us-east-2", # or set dynamically if needed
            "aws_access_key": aws_access_key,
            "aws_secret_key": aws_secret_key,
            "aws_session_token": aws_session_token,
            "image_type": image_type
        }
    }

    try:
        response = requests.post(aap_url, headers=headers, json=payload)
    except Exception as e:
        print(f"Exception calling AAP API: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Failed to call AAP API"}),
        }

    if response.status_code in [200, 201, 202]:
        print("✅ AAP job triggered successfully!")
    else:
        print(f"❌ Failed to trigger AAP: {response.status_code} - {response.text}")

    return {
        "statusCode": response.status_code,
        "body": json.dumps({
            "message": "Webhook processed",
            "aap_response": response.text
        }),
    }