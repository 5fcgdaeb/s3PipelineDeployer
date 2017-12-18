Here is a nice and quick Continous Deployment tool if your project has the following setup:
1) Your website is being hosted on AWS S3 Bucket (it is free!)
2) You are using Bitbucket to host your code/repository

With this Bitbucket pipeline and Python script:
- Your changes to your website are automatically deployed to the S3 Bucket
- Only the modified files are uploaded to S3; making sure that you don't go over your AWS S3 Free Tier limits
- CSS and Javascript files are first compressed before being uploaded

Future Work:
- If a file is deleted from the repository, remove the deleted file from S3 Bucket