import json
import logging
import os

# Logging configuration
logger = logging.getLogger()
if logger.hasHandlers():
    logger.setLevel(logging.INFO)

# Environment variables
ImportServiceRole = os.environ["ImportServiceRole"]
NotificationSQSQueue = os.environ["NotificationSQSQueue"]

# AWS service resources and clients
ec2_client = boto3.client("ec2")
sqs_client = boto3.client("sqs")

# Event handler
def lambda_handler(event, context):
    logger.info(f"Processing event {event}")
  
    for record in event["Records"]:
        handle_record(record)

# Record handler
def handle_record(record):
    logger.info(f"Processing record {record}")

    bucket = record['s3']['bucket']['name']
    key = record['s3']['object']['key']

    response = ec2_client.import_image(
      DiskContainers=[
          {
              "Format": key.split(".")[-1],
              "UserBucket": {
                  "S3Bucket": bucket,
                  "S3Key": key  
              }
          }
      ],
      LicenseType="BYOL",
      RoleName=ImportServiceRole,
      BootMode='legacy-bios'
  
  )

  logger.info(response)

  sqs_client.send_message(
        QueueUrl=NotificationsSQSQueue,
        MessageBody=json.dumps(response)
  )
