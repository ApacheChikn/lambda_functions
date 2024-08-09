import json
import boto3
from typing import List, Optional

# Import the Boto3 library to interact with AWS services

def get_ec2_client() -> boto3.client:
    """
    Creates and returns an EC2 client using Boto3.

    Returns:
        boto3.client: The EC2 client.
    """
    return boto3.client('ec2')

def get_s3_client() -> boto3.client:
    """
    Creates and returns an S3 client using Boto3.

    Returns:
        boto3.client: The S3 client.
    """
    return boto3.client('s3')

def describe_instances(client: boto3.client) -> List[dict]:
    """
    Describes EC2 instances and returns a list of instances.

    Args:
        client (boto3.client): The EC2 client used to describe instances.

    Returns:
        List[dict]: A list of instances.
    """
    response = client.describe_instances()  # Call the describe_instances method to get information about EC2 instances
    instances = []
    for reservation in response['Reservations']:  # Iterate over each reservation in the response
        instances.extend(reservation['Instances'])  # Extend the instances list with instances from the reservation
    return instances

def create_ubuntu_instance(client: boto3.client) -> None:
    """
    Creates an Ubuntu EC2 instance.

    Args:
        client (boto3.client): The EC2 client used to create the instance.

    Returns:
        None
    """
    user_data = '''#!/bin/bash
        apt update -y
        apt-get install -y apache2
        systemctl start apache2
        systemctl enable apache2'''
        
    create_instance(client, "ami-09e67e426f25ce0d7", user_data=user_data)  # Call create_instance with the Ubuntu AMI ID

def create_amazon_linux_2023_instance(client: boto3.client) -> None:
    """
    Creates an Amazon Linux 2023 EC2 instance.

    Args:
        client (boto3.client): The EC2 client used to create the instance.

    Returns:
        None
    """
    create_instance(client, "ami-08a0d1e16fc3f61ea")  # Call create_instance with the Amazon Linux 2023 AMI ID

def create_amazon_linux_2_instance(client: boto3.client) -> None:
    """
    Creates an Amazon Linux 2 EC2 instance.

    Args:
        client (boto3.client): The EC2 client used to create the instance.

    Returns:
        None
    """
    create_instance(client, "ami-0eaf7c3456e7b5b68")  # Call create_instance with the Amazon Linux 2 AMI ID

def create_instance(client: boto3.client, ami: str, user_data: Optional[str] = None) -> None:
    """
    Creates an EC2 instance with the specified AMI.

    Args:
        client (boto3.client): The EC2 client used to create the instance.
        ami (str): The AMI ID to use for the instance.
        user_data (Optional[str]): The user data script to run on the instance. Defaults to None.

    Returns:
        None
    """
    key_name = 'private-ec2'  # Key pair name for the instance
    
    if user_data is None:
        client.run_instances(
            MaxCount=1,
            MinCount=1,
            ImageId=ami,
            InstanceType="t2.micro",
            KeyName=key_name,
            SecurityGroupIds=['sg-0197b8159a5d886f8']  # Security group for the instance
        )
    else:
        client.run_instances(
            MaxCount=1,
            MinCount=1,
            ImageId=ami,
            InstanceType="t2.micro",
            KeyName=key_name,
            UserData=user_data,
            SecurityGroupIds=['sg-0197b8159a5d886f8']  # Security group for the instance
        )
        
def list_buckets(s3_client: boto3.client) -> List[str]:
    """
    Lists the names of all S3 buckets.

    Args:
        s3_client (boto3.client): The S3 client used to list buckets.

    Returns:
        List[str]: A list of bucket names.
    """
    response = s3_client.list_buckets()  # Call the list_buckets method to get information about S3 buckets
    return [bucket['Name'] for bucket in response['Buckets']]  # Extract and return the list of bucket names
    
def create_instances(ec2_client: boto3.client, instance_type: str = "ubuntu", instance_amount: int = 1) -> None:
    """
    Create EC2 instances of the specified type and amount using the provided EC2 client.

    Args:
        ec2_client (boto3.client): The EC2 client used to create instances.
        instance_type (str): The type of instance to create. Defaults to "ubuntu".
        instance_amount (int): The number of instances to create. Defaults to 1.
    
    Returns:
        None
    """
    for i in range(instance_amount):
        if instance_type.lower() == "ubuntu":
            create_ubuntu_instance(ec2_client)  # Create an Ubuntu instance
            print("Created instance type:", instance_type)
        elif instance_type.lower() == "linux 2023":
            create_amazon_linux_2023_instance(ec2_client)  # Create an Amazon Linux 2023 instance
            print("Created instance type:", instance_type)
        elif instance_type.lower() == "linux 2":
            create_amazon_linux_2_instance(ec2_client)  # Create an Amazon Linux 2 instance
            print("Created instance type:", instance_type)
        else:
            print("Unsupported instance type", instance_type)  # Handle unsupported instance types

def lambda_handler(event: dict, context: dict) -> dict:
    """
    AWS Lambda function handler to create EC2 instances.

    Args:
        event (dict): The event data that triggered the Lambda function.
        context (dict): The context in which the Lambda function is executed.

    Returns:
        dict: A response object with a status code and a message.
    """
    ec2_client = get_ec2_client()  # Retrieve the EC2 client
    instance_type = "ubuntu"  # Specify the instance type
    instance_amount = 1  # Specify the number of instances to create
    create_instances(ec2_client, instance_type, instance_amount)  # Create the instances
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
