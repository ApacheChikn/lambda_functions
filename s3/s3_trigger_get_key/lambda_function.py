import json
import boto3

def lambda_handler(event, context):
    # Print the event object for debugging purposes
    print(event)
    
    # Extract the 'Records' field from the event
    records = event['Records']
    
    # Iterate through the records
    for record in records:
        # Extract the 'key' field from the S3 object in each record
        key = record['s3']['object']['key']
    
        # Print the key value for each S3 object
        print(key)
