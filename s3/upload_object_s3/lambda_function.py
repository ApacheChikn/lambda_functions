import json
import boto3

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    # TODO implement
    filename = 'lambda_function.py'
    bucket_name="zali-catch-all"
    
    with open(filename, 'rb') as data:
        s3.upload_fileobj(data, bucket_name, filename)
        print("Object Uploaded")