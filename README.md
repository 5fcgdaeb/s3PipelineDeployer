Here is a nice and quick <b>Continous Deployment</b> tool if your project has the following setup:
- Your website is being hosted on AWS S3 Bucket (it is free!)
- You are using Bitbucket to host your code/repository

With this Bitbucket pipeline && Python script:
- Your changes to your website are automatically deployed to the S3 Bucket
- Only the modified files are uploaded to S3; making sure that you don't go over your AWS S3 Free Tier limits
- CSS and Javascript files are first compressed before being uploaded

How to use:
1) Setup your Bitbucket repository to have a pipeline; use the bitbucket-pipelines.yml file as the configuration file
2) Add s3Deployer.py file to your repository

Future Work:
- If a file is deleted from the repository, remove the deleted file from S3 Bucket as well