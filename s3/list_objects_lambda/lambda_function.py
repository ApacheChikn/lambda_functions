import json
import boto3

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    
    try:
        bucket_name=event['queryStringParameters']['bucket_name']
    except:
        return { 'body' : json.dumps("No bucket_name present")}
    
    try:
        response = s3.list_objects(
            Bucket=bucket_name
        )
    except:
        return { 'body' : json.dumps("bucket_name not valid")}
    
    
    contents = response['Contents']
    key_names = []
    
    for content in contents:
        print(content['Key'])
        key_names.append(content['Key'])
    
    
    return {
        'body': json.dumps(key_names)
    }
