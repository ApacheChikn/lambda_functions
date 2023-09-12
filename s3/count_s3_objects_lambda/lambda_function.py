import boto3
import json

s3 = boto3.client('s3')

def lambda_handler(event, context):
    
    response = s3.list_objects(Bucket='zali-catch-all')
    
    Contents = response['Contents']
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('zali-catch-all has ' + str(len(Contents)) + " objects!")
    }