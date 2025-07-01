# This lambda function will not only export the S3 Key of the uploaded file,
# but it will also export the current aws access key and secret key in a secure manner. 

import json
import requests
import boto3
from botocore.exceptions import ClientError


def get_secret():
    secret_name = "aap_api_key"
    region_name = "us-east-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    secret = get_secret_value_response['SecretString']
    return secret


def lambda_handler(event, context):
    key = event['Records'][0]['s3']['object']['key']
    api_secret = get_secret()

    print(f"Triggering AAP job via API launch for key: {key}")

    # Get temporary AWS credentials from Lambda's execution role
    credentials = boto3.Session().get_credentials().get_frozen_credentials()
    aws_access_key = credentials.access_key
    aws_secret_key = credentials.secret_key
    aws_session_token = credentials.token

    # AAP API endpoint
    job_template_id = 42
    aap_url = f"https://aap-aap.apps.cluster-wb8g6-1.dynamic.redhatworkshops.io/api/controller/v2/job_templates/{job_template_id}/launch/"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_secret}"
    }

    # Include all required vars in payload
    payload = {
        "extra_vars": {
            "s3_key": key,
            "aws_access_key": aws_access_key,
            "aws_secret_key": aws_secret_key,
            "aws_session_token": aws_session_token
        }
    }

    response = requests.post(aap_url, headers=headers, data=json.dumps(payload))

    if response.status_code in [200, 201, 202]:
        print("✅ AAP job triggered successfully!")
        print(json.dumps(payload, indent=2))
        print(aws_access_key)
        print(aws_secret_key)
    else:
        print(f"❌ Failed to trigger AAP: {response.status_code} - {response.text}")

    return {
        'statusCode': response.status_code,
        'body': response.text
    }
