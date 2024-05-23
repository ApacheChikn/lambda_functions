import json
import boto3
import time
from typing import Any, Dict, Optional

def create_log_group(cw_client: boto3.client, lg_name: str) -> Dict[str, Any]:
    """
    Create a CloudWatch log group.

    Parameters:
    cw_client (boto3.client): The CloudWatch Logs client.
    lg_name (str): The name of the log group.

    Returns:
    Dict[str, Any]: The response from the create_log_group call.
    """
    try:
        response = cw_client.create_log_group(logGroupName=lg_name)
        return response
    except cw_client.exceptions.ResourceAlreadyExistsException as e:
        print(e)

def create_log_stream(cw_client: boto3.client, lg_name: str, ls_name: str) -> Dict[str, Any]:
    """
    Create a CloudWatch log stream.

    Parameters:
    cw_client (boto3.client): The CloudWatch Logs client.
    lg_name (str): The name of the log group.
    ls_name (str): The name of the log stream.

    Returns:
    Dict[str, Any]: The response from the create_log_stream call.
    """
    try:
        response = cw_client.create_log_stream(logGroupName=lg_name, logStreamName=ls_name)
        return response
    except cw_client.exceptions.ResourceAlreadyExistsException as e:
        print(e)

def put_log_events(cw_client: boto3.client, lg_name: str, ls_name: str, message: str = "", timestamp: Optional[int] = None) -> Dict[str, Any]:
    """
    Put log events to a CloudWatch log stream.

    Parameters:
    cw_client (boto3.client): The CloudWatch Logs client.
    lg_name (str): The name of the log group.
    ls_name (str): The name of the log stream.
    message (str): The log message.
    timestamp (Optional[int]): The timestamp for the log event. Defaults to current time if not provided.

    Returns:
    Dict[str, Any]: The response from the put_log_events call.
    """
    if timestamp is None:
        timestamp = round(time.time() * 1000)
    try:
        response = cw_client.put_log_events(
            logGroupName=lg_name,
            logStreamName=ls_name,
            logEvents=[
                {
                    'timestamp': timestamp,
                    'message': message
                },
            ]
        )
        return response
    except cw_client.exceptions.ResourceAlreadyExistsException as e:
        print(e)

def lambda_handler(event: Dict[str, Any], context: Any) -> None:
    """
    Lambda function handler to create a log group, log stream, and put log events.

    Parameters:
    event (Dict[str, Any]): The event data passed to the Lambda function.
    context (Any): The context in which the Lambda function is running.
    """
    cloudwatch_logs = boto3.client('logs')
    
    lg_name = 'lg_from_lambda'
    ls_name = 'ls_from_lambda'

    # Create a log group
    create_log_group(cloudwatch_logs, lg_name)

    # Create a log stream within the log group
    create_log_stream(cloudwatch_logs, lg_name, ls_name)

    # Put a log event to the log stream
    put_log_events(cloudwatch_logs, lg_name, ls_name, message="Message from Lambda")
