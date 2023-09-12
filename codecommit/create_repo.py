import json
import boto3
import uuid

def lambda_handler(event, context):
    # Create a CodeCommit client
    codecommit = boto3.client('codecommit')
    
    # Create a new CodeCommit repository with the specified name
    response = codecommit.create_repository(
        repositoryName='zali-boto3-{}'.format(str(uuid.uuid4()))
    )
    
    # Print the response from the repository creation
    print(response)
    
    # Remove unnecessary fields from the response
    del response["repositoryMetadata"]["lastModifiedDate"]
    del response["repositoryMetadata"]["creationDate"]
    
    # TODO: Implement the rest of your Lambda function logic here
    
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
