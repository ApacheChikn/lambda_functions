import json
import boto3
from typing import Any, Dict, List

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler to stop all running EC2 instances.

    Args:
        event (Dict[str, Any]): The event that triggered the Lambda function.
        context (Any): The runtime information of the Lambda function.

    Returns:
        Dict[str, Any]: The response object containing the status code and the 
        body with either the result of the stop instances operation or a message 
        indicating no running instances were found.
    """
    
    # Initialize EC2 client
    ec2 = boto3.client('ec2')
    
    # List to store the instance IDs of running instances
    running_instance_ids: List[str] = []
    
    # Describe instances with the 'running' state
    instances = ec2.describe_instances(
        Filters=[
            { "Name": "instance-state-name", "Values": ["running"] }
        ]
    )
    
    # Loop through the reservations and instances to collect running instance IDs
    for reservation in instances["Reservations"]:
        for instance in reservation["Instances"]:
            print(instance['InstanceId'])
            running_instance_ids.append(instance['InstanceId'])
    
    # If there are running instances, stop them
    if len(running_instance_ids) > 0:
        response = ec2.stop_instances(InstanceIds=running_instance_ids)
    
        print(response)
    
        return {
            'statusCode': 200,
            'body': json.dumps(response, indent=4)
        }
    else:
        msg = "No running instances"
        print(msg)
        return {
            'statusCode': 200,
            'body': msg
        }
