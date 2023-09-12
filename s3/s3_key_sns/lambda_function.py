import json
import boto3
import os

sns = boto3.client('sns')
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']

def get_key(record):
    s3_dict = record['s3']
    obj_dict = s3_dict['object']
    key = obj_dict['key']
    return key

def lambda_handler(event, context):
    # TODO implement
    
    Records = event['Records']
    
    for Record in Records:
        key = get_key(Record)
        
        print(key)
        response = sns.publish(TopicArn=SNS_TOPIC_ARN, Message=key)