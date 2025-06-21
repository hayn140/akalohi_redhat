Your S3 Bucket needs to be set up with the correct ACL Permissions.

Refer to Page 49 (https://docs.aws.amazon.com/pdfs/vm-import/latest/userguide/vm-import-ug.pdf#image-import)

1. Object Ownership
    a. ACLs enabled
    b. Object Ownership: Object Writer

2. Access control list (ACL)
    a. Add Grantee
        i. Use Canonical ID for 'All other Regions'
        - All other Regions Canonical ID:     
        -  c4d8eabf8db69dbe46bfe0e517100c554f01200b104d59cd408e777ba442a322
    b. For each Grantee, provide the following permissions:
        - READ_ACP (In the Amazon S3 console, Bucket ACL should have the Read permission)
        - WRITE (In the Amazon S3 console, Objects should have the Write permission)

3. Setup vmimport IAM role

#####trust-policy.json#####

---------------------------------------------------------

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "vmie.amazonaws.com"
            },
            "Action": "sts:AssumeRole",
            "Condition": {
                "StringEquals": {
                    "sts:Externalid": "vmimport"
                }
            }
        }
    ]
}

---------------------------------------------------------

#####role-policy.json##### *substitute your bucket name*

---------------------------------------------------------

{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Effect": "Allow",
			"Action": [
				"s3:GetBucketLocation",
				"s3:GetObject",
				"s3:PutObject"
			],
			"Resource": [
				"arn:aws:s3:::akalohi-aws-bucket-1",
				"arn:aws:s3:::akalohi-aws-bucket-1/*"
			]
		},
		{
			"Effect": "Allow",
			"Action": [
				"ec2:CancelConversionTask",
				"ec2:CancelExportTask",
				"ec2:CreateImage",
				"ec2:CreateInstanceExportTask",
				"ec2:CreateTags",
				"ec2:DescribeConversionTasks",
				"ec2:DescribeExportTasks",
				"ec2:DescribeExportImageTasks",
				"ec2:DescribeImages",
				"ec2:DescribeInstanceStatus",
				"ec2:DescribeInstances",
				"ec2:DescribeSnapshots",
				"ec2:DescribeTags",
				"ec2:ExportImage",
				"ec2:ImportInstance",
				"ec2:ImportVolume",
				"ec2:StartInstances",
				"ec2:StopInstances",
				"ec2:TerminateInstances",
				"ec2:ImportImage",
				"ec2:ImportSnapshot",
				"ec2:DescribeImportImageTasks",
				"ec2:DescribeImportSnapshotTasks",
				"ec2:CancelImportTask"
			],
			"Resource": "*"
		}
	]
}

---------------------------------------------------------