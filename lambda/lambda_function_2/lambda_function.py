# This lambda function sends AAP the following ansible variables
#   - s3_key : Key of the uploaded file (Triggered by a .vmdk uploaded in 'networkB-images' S3 Bucket at Imports/)
#   - s3_bucket : AWS Bucket name
#   - aws_region: AWS Region
#   - aws_access_key : credentials
#   - aws_secret_key : credentials
#   - aws_session_token: credentials
#   - image_type : The type of image being uploaded
#   - image_name : The name of the image, to be used for naming final provisioned images

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
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    return get_secret_value_response['SecretString']

def extract_image_name(key):
    # Extract the base name of the file (without directory path)
    base_name = os.path.basename(key)
    # Extract the name without the extension
    image_name, _ = os.path.splitext(base_name)
    return image_name

def lambda_handler(event, context):
    # Extract S3 object info
    key = event['Records'][0]['s3']['object']['key']
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    region = event['Records'][0]['awsRegion']
    api_secret = get_secret()

    print(f"Triggering AAP job via API launch for s3_key: {key}, bucket: {bucket_name}, region: {region}")

    # Extract file extension (e.g., 'ova')
    _, ext = os.path.splitext(key)
    image_type = ext.lstrip('.').lower()  # 'ova', 'vmdk', etc.

    # Extract image name from the key
    image_name = extract_image_name(key)

    # Get temporary AWS credentials
    credentials = boto3.Session().get_credentials().get_frozen_credentials()
    aws_access_key = credentials.access_key
    aws_secret_key = credentials.secret_key
    aws_session_token = credentials.token

    # AAP API endpoint
    job_template_id = 130
    aap_url = f""

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_secret}"
    }

    # Payload with s3 info, region, and image name
    payload = {
        "extra_vars": {
            "s3_key": key,
            "s3_bucket_name": bucket_name,
            "aws_region": region,
            "aws_access_key": aws_access_key,
            "aws_secret_key": aws_secret_key,
            "aws_session_token": aws_session_token,
            "image_type": image_type,
            "image_name": image_name 
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

