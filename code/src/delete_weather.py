import json
import boto3
import os

from src.message import *


def lambda_handler(event, context):
    try:
        dynamodb = boto3.client('dynamodb')
        # get table name
        dynamodb_table = os.environ['DYNAMODB_TABLE']
        # Extract the 'id' parameter from the path parameters
        id_param = event['pathParameters']['id']

        # Delete the record from DynamoDB
        dynamodb.delete_item(
            TableName=dynamodb_table,
            Key={'id': {'S': id_param}}
        )

        response = {
            'statusCode': 200,
            'body': json.dumps(MSG_06)
        }
        
    except Exception as e:
        response = {
            'statusCode': 500,
            'body': json.dumps(MSG_05.format(e=str(e)))
        }

    return response
