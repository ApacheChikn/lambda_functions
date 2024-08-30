import json
import boto3
import uuid
from typing import Any, Dict

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda function to create a security group in EC2 and authorize HTTP access.

    This function creates a new security group with a unique name, allows ingress on port 80 (HTTP) 
    from any IP address, and returns the response from the authorize security group ingress operation.

    Args:
        event (dict): AWS Lambda event data (not used in this function).
        context (Any): AWS Lambda context object (not used in this function).

    Returns:
        dict: HTTP response containing the status code and details of the authorized security group ingress.
    """
    # Initialize EC2 client
    ec2 = boto3.client('ec2')
    
    # Create a new security group with a unique name
    response = ec2.create_security_group(
        Description='security group from lambda',
        GroupName='sglambda' + str(uuid.uuid4())[24:]
    )
    
    # Extract the security group ID from the response
    group_id = response['GroupId']
    
    # Authorize HTTP ingress from any IP address
    response = ec2.authorize_security_group_ingress(
        GroupId=group_id,
        IpPermissions=[
            {
                'FromPort': 80,
                'IpProtocol': 'tcp',
                'IpRanges': [
                    {
                        'CidrIp': '0.0.0.0/0',
                        'Description': 'HTTP ACCESS'
                    },
                ],
                'ToPort': 80
            },
        ],
    )

    # Return the response as a JSON object with status code 200
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
