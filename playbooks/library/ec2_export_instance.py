import boto3
from botocore.exceptions import ClientError
from ansible.module_utils.basic import AnsibleModule

def run_module():
    module_args = dict(
        instance_id=dict(type='str', required=True),
        disk_image_format=dict(type='str', required=True),
        s3_bucket=dict(type='str', required=True),
        s3_prefix=dict(type='str', required=True),
        target_environment=dict(type='str', required=True),
        region=dict(type='str', required=False, default='us-east-1'),
        description=dict(type='str', required=False, default='Export instance to S3')
    )

    result = dict(
        changed=False,
        msg='',
        export_task_id='',
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    s3_bucket = module.params['s3_bucket']

    try:
        # Step 1: Set S3 bucket ACL
        s3 = boto3.client('s3', region_name=module.params['region'])

        s3.put_bucket_acl(
            Bucket=module.params['s3_bucket'],
            GrantRead='uri="http://acs.amazonaws.com/groups/global/AllUsers"',
            GrantWrite='uri="http://acs.amazonaws.com/groups/global/AllUsers"'
        )

        # Step 2: Run export task
        ec2 = boto3.client('ec2', region_name=module.params['region'])

        response = ec2.create_instance_export_task(
            Description=module.params['description'],
            InstanceId=module.params['instance_id'],
            TargetEnvironment=module.params['target_environment'],
            ExportToS3Task={
                'DiskImageFormat': module.params['disk_image_format'],
                'S3Bucket': module.params['s3_bucket'],
                'S3Prefix': module.params['s3_prefix']
            }
        )

        result['export_task_id'] = response.get('ExportTask', {}).get('ExportTaskId', '')
        result['changed'] = True
        result['msg'] = f"Export task started: {result['export_task_id']}"

    except ClientError as e:
        module.fail_json(msg=f"AWS error: {str(e)}", **result)
    except Exception as e:
        module.fail_json(msg=f"Unexpected error: {str(e)}", **result)

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
