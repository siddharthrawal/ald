import json
import boto3
import os

from src.message import *



def lambda_handler(event, context):

    try:
        dynamodb = boto3.client('dynamodb')
        # get table name
        dynamodb_table = os.environ['DYNAMODB_TABLE']
        # Parse the incoming API Gateway event
        request_body = json.loads(event['body'])
        if not request_body:
            response = {
                    'statusCode': 400,
                    'body': json.dumps(MSG_03.format(attr=attr))
                }
            return response
        # get parameters
        id = request_body.get('id', None)
        weather = request_body.get('Weather', None)
        # validation
        allowed_attributes = ['id', 'Weather']
        for attr in request_body.keys():
            if attr not in allowed_attributes:
                response = {
                    'statusCode': 400,
                    'body': json.dumps(MSG_03.format(attr=attr))
                }
                return response
        if not id :
            response = {
                'statusCode': 400,
                'body': json.dumps(MSG_01)
            }
            return response
        
        if not weather :
            response = {
                'statusCode': 400,
                'body': json.dumps(MSG_02)
            }
            return response
        



        # Extract data from the request body
        item = {
            'id': {'S': id},
            'temperature': {'S': str(weather)}
        }

        # Insert data into DynamoDB
        dynamodb.put_item(
            TableName=dynamodb_table,
            Item=item
        )

        response = {
            'statusCode': 200,
            'body': json.dumps(MSG_04)
        }
    except Exception as e:
        response = {
            'statusCode': 500,
            'body': json.dumps(MSG_05.format(e=str(e)))
        }
    
    return response
