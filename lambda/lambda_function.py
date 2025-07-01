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
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = get_secret_value_response['SecretString']
    return secret

def lambda_handler(event, context):
    key = event['Records'][0]['s3']['object']['key']
    api_secret = get_secret()
    
    print(f"Triggering AAP job via API launch for key: {key}")

    # AAP direct API endpoint (no webhook key here)
    job_template_id = 42
    aap_url = f"https://aap-aap.apps.cluster-wb8g6-1.dynamic.redhatworkshops.io/api/controller/v2/job_templates/{job_template_id}/launch/"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_secret}"
    }

    payload = {
        "extra_vars": {
            "s3_key": key
        }
    }

    response = requests.post(aap_url, headers=headers, data=json.dumps(payload))

    if response.status_code in [200, 201, 202]:
        print("✅ AAP job triggered successfully!")
        print(json.dumps(payload, indent=2))

    else:
        print(f"❌ Failed to trigger AAP: {response.status_code} - {response.text}")

    return {
        'statusCode': response.status_code,
        'body': response.text
    }
