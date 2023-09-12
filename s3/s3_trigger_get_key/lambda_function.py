import json
import boto3

def lambda_handler(event, context):
    records = event['Records']
    
    for record in records:
        key = record['s3']['object']['key']
    
        print(key)