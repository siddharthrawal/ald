import json
import pytest
import boto3
from botocore.exceptions import BotoCoreError
from src.delete_weather import lambda_handler
from src.message import *

@pytest.fixture
def dynamodb_mock(mocker):
    return mocker.patch('boto3.client')

def test_successful_delete(dynamodb_mock):
    event = {
        'pathParameters': {'id': '123'}
    }
    context = {}

    actual_response = lambda_handler(event, context)

    expected_response = {
        'statusCode': 200,
        'body': MSG_06
    }
    # Parse the JSON strings
    actual_response_body_parsed = json.loads(actual_response['body'])
    expected_response_body = expected_response['body']
    assert actual_response_body_parsed == expected_response_body
    assert actual_response['statusCode'] == expected_response['statusCode']

    # Ensure that delete_item was called with the correct parameters
    dynamodb_mock.return_value.delete_item.assert_called_once_with(
        TableName='Weather',
        Key={'id': {'S': '123'}}
    )

def test_delete_error(dynamodb_mock):
    event = {
        'pathParameters': {'id': '123'},
        'ResourceProperties': {'DynamoDBTable': 'WeatherData'}
    }
    context = {}

    # Mock the delete_item method to raise a BotoCoreError
    dynamodb_mock.return_value.delete_item.side_effect = BotoCoreError()

    response = lambda_handler(event, context)

    assert response == {
        'statusCode': 500,
        'body': '"Error inserting data: An unspecified error occurred"'
    }

    # Ensure that delete_item was called once
    dynamodb_mock.return_value.delete_item.assert_called_once_with(
        TableName='Weather',
        Key={'id': {'S': '123'}}
    )
