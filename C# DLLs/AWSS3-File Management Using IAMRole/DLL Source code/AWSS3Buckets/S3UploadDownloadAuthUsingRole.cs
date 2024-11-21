using Amazon;
using Amazon.S3;
using Amazon.S3.Model;
using Amazon.SecurityToken;
using Amazon.SecurityToken.Model;
using System;

namespace AWSS3Buckets
{
    public class S3UploadDownloadAuthUsingRole
    {
        public string BucketName { get; set; }
        public string UploadFileName { get; set; }
        public string UploadFilePath { get; set; }
        public string DownloadFileName { get; set; }
        public string DeleteFileName { get; set; }
        public string DownloadFilePath { get; set; }
        public string CreateBucket { get; set; }
        public string RoleArn { get; set; }  // IAM Role ARN
        public string SessionName { get; set; } // Session Name for the assumed role
        public string Region { get; set; }

        // Function to assume role and get temporary credentials
        private AmazonS3Client GetS3ClientWithRole()
        {
            if (string.IsNullOrEmpty(this.Region))
                throw new ArgumentException("Please enter Region field");
            if (string.IsNullOrEmpty(this.RoleArn))
                throw new ArgumentException("Please enter RoleArn field");

            RegionEndpoint regionEndpoint = RegionEndpoint.GetBySystemName(this.Region);
            if (regionEndpoint.DisplayName == "Unknown")
                throw new ArgumentException("Please enter valid Region field");

            try
            {
                // Assume Role via AWS STS
                var stsClient = new AmazonSecurityTokenServiceClient(regionEndpoint);
                var assumeRoleRequest = new AssumeRoleRequest
                {
                    RoleArn = this.RoleArn,
                    RoleSessionName = this.SessionName ?? "S3Session"
                };

                var assumeRoleResponse = stsClient.AssumeRole(assumeRoleRequest);
                var credentials = assumeRoleResponse.Credentials;

                // Return an S3 client using the assumed role credentials
                return new AmazonS3Client(credentials.AccessKeyId, credentials.SecretAccessKey, credentials.SessionToken, regionEndpoint);
            }
            catch (Exception ex)
            {
                throw new Exception($"Error assuming role: {ex.Message}");
            }
        }

        // Upload file to S3
        public string UploadToS3()
        {
            if (string.IsNullOrEmpty(this.BucketName))
                return "Please enter BucketName field";
            if (string.IsNullOrEmpty(this.UploadFileName))
                return "Please enter UploadFileName field";

            AmazonS3Client amazonS3Client;
            try
            {
                amazonS3Client = GetS3ClientWithRole(); // Get S3 client using assumed role
            }
            catch (Exception ex)
            {
                return ex.Message;
            }

            try
            {
                PutObjectRequest request = new PutObjectRequest()
                {
                    BucketName = this.BucketName,
                    Key = this.UploadFileName,
                    FilePath = this.UploadFilePath,
                    ContentType = "text/plain"
                };
                amazonS3Client.PutObject(request);
            }
            catch (AmazonS3Exception ex)
            {
                return "There was an error uploading file to the S3 bucket. Here is the detailed message : " + ex.Message;
            }

            return "File successfully uploaded to the S3 bucket";
        }

        // Download file from S3
        public string DownloadFromS3()
        {
            if (string.IsNullOrEmpty(this.BucketName))
                return "Please enter BucketName field";
            if (string.IsNullOrEmpty(this.DownloadFileName))
                return "Please enter DownloadFileName field";

            AmazonS3Client amazonS3Client;
            try
            {
                amazonS3Client = GetS3ClientWithRole(); // Get S3 client using assumed role
            }
            catch (Exception ex)
            {
                return ex.Message;
            }

            try
            {
                GetObjectRequest request = new GetObjectRequest()
                {
                    BucketName = this.BucketName,
                    Key = this.DownloadFileName
                };
                amazonS3Client.GetObject(request).WriteResponseStreamToFile(this.DownloadFilePath);
            }
            catch (AmazonS3Exception ex)
            {
                return "There was an error downloading file from the S3 bucket. Here is the detailed message : " + ex.Message;
            }

            return "File successfully downloaded from the S3 bucket";
        }

        // Delete file from S3
        public string DeleteFromS3()
        {
            if (string.IsNullOrEmpty(this.BucketName))
                return "Please enter BucketName field";
            if (string.IsNullOrEmpty(this.DeleteFileName))
                return "Please enter DeleteFileName field";

            AmazonS3Client amazonS3Client;
            try
            {
                amazonS3Client = GetS3ClientWithRole(); // Get S3 client using assumed role
            }
            catch (Exception ex)
            {
                return ex.Message;
            }

            try
            {
                DeleteObjectRequest request = new DeleteObjectRequest()
                {
                    BucketName = this.BucketName,
                    Key = this.DeleteFileName
                };
                amazonS3Client.DeleteObject(request);
            }
            catch (AmazonS3Exception ex)
            {
                return "There was an error deleting file from the S3 bucket. Here is the detailed message : " + ex.Message;
            }

            return "File successfully deleted from the S3 bucket";
        }
    }
}
