import boto3
import json

s3 = boto3.client('s3')
def lambda_handler(event, context):
    # TODO implement
    
    print("lambda ran")
    
    records = event["Records"]
    
    for record in records:
        key = record['s3']['object']['key']
        
        html = "<html><br><h1>This was made in Lambda</h1><br><h2>The last object created was: " + key + " </h2></html>"
        
        print(key)
        
        s3.put_object(Body=html, Bucket='zali-catch-all', Key='index.html', ContentType='text/html', ACL='public-read')

    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
