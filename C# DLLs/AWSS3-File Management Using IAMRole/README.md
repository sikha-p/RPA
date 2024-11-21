# AWSS3-Bucket- File Download , Upload & Delete using IAM Role
This folder the DLL source code & sample A360 to do AWS S3 File management operations including upload , download and delete using IAM Role instead of using IAM User credentials.

You can utilize the AssumeRole feature to access AWS s3 instead of IAM User. AssumeRole is an API operation provided by the AWS Security Token Service (STS) that returns a set of temporary security credentials for an IAM role. These credentials consist of an access key ID, a secret access key, and a session token. You can use these temporary credentials to make authenticated requests to AWS services.
https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html

**What is roleArn?**
- roleArn stands for Role Amazon Resource Name. An ARN is a unique identifier for an AWS resource. A role ARN specifically refers to the ARN of an IAM role in AWS. It uniquely identifies the role within your AWS account and can be used to assume the role for temporary access to AWS resources.

- The format of a role ARN is as follows:

       arn:aws:iam::account-id:role/role-name

     account-id is the 12-digit AWS account ID.
     role-name is the name of the IAM role.

- We currently have a DLL solution that connects to an Amazon S3 bucket for upload and download operations, which utilizes IAM user credentials (Access Key and Secret Key) for authentication. 
https://botstore.automationanywhere.com/bot/automation-360-aws-s3-file-management

- So instead of using IAM role you can utilize IAM role AssumeRole feature to access S3 bucket resources. 

**Please find the DLL details below,**

- Namespace : AWSS3Buckets
- Classname : S3UploadDownloadAuthUsingRole

The main DLL has 2 dependant files
AWSSDK.S3.dll
AWSSDK.Core.dll

Use below Amazon documentation link to get the region system name (2nd column in the table)
https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.RegionsAndAvailabilityZones.html

![image](https://github.com/partnersolutiondesk/RPA/assets/84059776/a97ec5bc-3ce4-4189-a7ac-8cc411de42f1)


