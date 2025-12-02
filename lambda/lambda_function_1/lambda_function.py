# This lambda function sends AAP the following ansible variables
#   - filename : Name of the VMDK file that arrived at /var/lib/portkey/temp_data on RHSAT02, sent to Lambda via curl POST method
#   - aws_access_key : credentials
#   - aws_secret_key : credentials
#   - aws_session_token: credentials

import json
import os
import requests
import boto3
from botocore.exceptions import ClientError

def get_secret():
    secret_name = ""
    region_name = ""

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name,
        verify='cert.pem'  # This cert.pem is used for AWS CA Bundle
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    return get_secret_value_response['SecretString']

def lambda_handler(event, context):
    api_secret = get_secret()
    filename = event['filename']

    # Get temporary AWS credentials
    credentials = boto3.Session().get_credentials().get_frozen_credentials()
    aws_access_key = credentials.access_key
    aws_secret_key = credentials.secret_key
    aws_session_token = credentials.token

    # AAP API endpoint
    job_template_id = 132
    aap_url = f""

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_secret}"
    }

    # Payload with s3 info, region, and image name
    payload = {
        "extra_vars": {
            "aws_access_key": aws_access_key,
            "aws_secret_key": aws_secret_key,
            "aws_session_token": aws_session_token,
            "filename": filename
        }
    }

    response = requests.post(aap_url, headers=headers, data=json.dumps(payload), verify='atp_bundle.pem')  # This atp_bundle.pem is used for NSA CA Bundle (All Trusted Partners)

    if response.status_code in [200]:
        print("✅ AAP job triggered successfully!")
    else:
        print(f"❌ Failed to trigger AAP: {response.status_code} - {response.text}")

    return {
        'statusCode': response.status_code
    }
