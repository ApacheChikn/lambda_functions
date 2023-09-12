import json
import boto3
import pandas as pd

def lambda_handler(event, context):
    # TODO implement
    s3 = boto3.client('s3')
    bucket = "zali-csv-s3"
    
    records = event["Records"]
    
    for record in records:
        key = record['s3']['object']['key']
        result = s3.get_object(Bucket=bucket, Key=key) 
        text = result["Body"].read().decode()
        
        print(text)
        data = pd.DataFrame([x.split(',') for x in text.split('\n')])
        
        response = data.iloc[1].to_string()

        print(response) 