import os, sys, argparse, tempfile, gzip
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import boto

def zipTheFileAndUpload(sourceFile, key):

    tempFile = tempfile.NamedTemporaryFile(mode="wb", suffix=".gz", delete=False)

    with open(sourceFile, 'rb') as f_in:
        with gzip.open(tempFile.name, 'wb') as gz_out:
            gz_out.writelines(f_in)

    key.set_metadata('Content-Type', 'application/x-javascript' if sourceFile.endswith(".js") else 'text/css')
    key.set_metadata('Content-Encoding', 'gzip')
    key.set_contents_from_filename(tempFile.name)

    os.unlink(tempFile.name)

def transferFile(sourceFile, bucketFile):

    if not os.path.isfile(sourceFile):
        print("File {0} no longer exists, skipping.".format(sourceFile))
        return

    if sourceFile.endswith(".js") or sourceFile.endswith(".css"):
        zipTheFileAndUpload(sourceFile, bucketFile)
    else:
        print("Uploading {0} to {1}".format(sourceFile, bucketFile.key))
        bucketFile.set_contents_from_filename(sourceFile)

def transferFilesToBucket(changedFiles, bucket):

    for file in changedFiles:

        fileWithoutNewLine = file.rstrip('\n')
        print("{0} was changed.".format(fileWithoutNewLine))

        fileShouldBeUploadedToS3 = True
        for fileToIgnore in ['.gitignore', 'bitbucket-pipelines.yml', 's3Deployer.py']: # slightly different content from gitignore
            if fileToIgnore in fileWithoutNewLine:
                fileShouldBeUploadedToS3 = False
                break

        if not fileShouldBeUploadedToS3:
            print("Not uploading {0} since it is not AWS S3 relevant.".format(fileWithoutNewLine))
            continue

        relativePath = fileWithoutNewLine.split("/")[-1]
        bucketFile = Key(bucket)
        bucketFile.key = relativePath

        if len(fileWithoutNewLine) < 1 or len(bucketFile.key) < 1:
            print("Not uploading file {0}, some problem with file.".format(file))
        else:
            transferFile(fileWithoutNewLine, bucketFile)

def main():

    arg_parser = argparse.ArgumentParser(description="Delta Deploy to AWS S3 Bucket")
    arg_parser.add_argument('-b','--bucket', help="Bucket Name in AWS S3", required=True)
    args = arg_parser.parse_args()

    conn = boto.s3.connect_to_region(
        boto.s3.connection.Location.EUCentral1, # Change this line for your S3 location
        calling_format=boto.s3.connection.OrdinaryCallingFormat())

    targetBucket = conn.get_bucket(args.bucket, validate=False)
    transferFilesToBucket(sys.stdin, targetBucket)

if __name__ == '__main__':
    main()