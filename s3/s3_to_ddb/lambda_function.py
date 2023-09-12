import boto3
import uuid

def lambda_handler(event, context):
    records = event["Records"]
    
    for record in records:
        if "s3" in record:
            bucket_name = record["s3"]["bucket"]["name"]  # Extract the name of the S3 bucket from the record
            object_key = record["s3"]["object"]["key"]  # Extract the object key from the record
            
            ddb = boto3.client('dynamodb')  # Create a DynamoDB client
            
            response = ddb.put_item(TableName='s3_keys', Item={
                    'id': {
                        'S': str(uuid.uuid4()),  # Generate a UUID as the ID for the DynamoDB item
                    },
                    'bucket': {
                        'S': bucket_name,  # Set the bucket name as a string attribute
                    },
                    'key': {
                        'S': object_key,  # Set the object key as a string attribute
                    },
                }
            )
