# This lambda function sends AAP the following
#   - s3_key : Key of the uploaded file (Triggered by a .ova uploaded in Imports/)
#   - s3_bucket : AWS Bucket name
#   - aws_region: AWS Region
#   - aws_access_key : credentials
#   - aws_secret_key : credentials
#   - aws_session_token: credentials
#   - 
import json
import requests
import boto3
from botocore.exceptions import ClientError

def get_secret():
    secret_name = "aap_api_key"
    region_name = "us-east-2"

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

    return get_secret_value_response['SecretString']

def lambda_handler(event, context):
    # Extract S3 object info
    key = event['Records'][0]['s3']['object']['key']
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    region = event['Records'][0]['awsRegion']
    api_secret = get_secret()

    print(f"Triggering AAP job via API launch for s3_key: {key}, bucket: {bucket_name}, region: {region}")

    # Get temporary AWS credentials
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

    # Payload with s3 info and region
    payload = {
        "extra_vars": {
            "s3_key": key,
            "s3_bucket_name": bucket_name,
            "aws_region": region,
            "aws_access_key": aws_access_key,
            "aws_secret_key": aws_secret_key,
            "aws_session_token": aws_session_token
        }
    }

    response = requests.post(aap_url, headers=headers, data=json.dumps(payload))

    if response.status_code in [200, 201, 202]:
        print("✅ AAP job triggered successfully!")
    else:
        print(f"❌ Failed to trigger AAP: {response.status_code} - {response.text}")

    return {
        'statusCode': response.status_code
    }
