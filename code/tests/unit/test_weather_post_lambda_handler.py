import json
import pytest
import boto3
from botocore.exceptions import BotoCoreError
from src.index import lambda_handler
from src.message import *

@pytest.fixture
def dynamodb_mock(mocker):
    return mocker.patch('boto3.client')

def test_successful_update(dynamodb_mock):
    event = {
        'body': '{"id": "123", "Weather": "Low Humidity"}'
    }
    expected_response = {'statusCode': 200, 'body': MSG_04}
    context = {}
    dynamodb_mock.return_value.put_item.return_value = {}
    actual_response = lambda_handler(event, context)
    # Parse the JSON strings
    actual_response_body_parsed = json.loads(actual_response['body'])
    expected_response_body = expected_response['body']
    assert actual_response_body_parsed == expected_response_body
    assert actual_response['statusCode'] == expected_response['statusCode']
    dynamodb_mock.return_value.put_item.assert_called_once()

def test_put_item_error(dynamodb_mock):
    event = {
        'body': '{"id": "123", "Weather": "Sunny day"}'
    }
    context = {}

    # Mock the put_item method to raise an error
    dynamodb_mock.return_value.put_item.side_effect = BotoCoreError()

    response = lambda_handler(event, context)

    assert response == {
        'statusCode': 500,
        'body': '"Error inserting data: An unspecified error occurred"'
    }

    # Ensure that put_item was called once
    dynamodb_mock.return_value.put_item.assert_called_once()

def test_missing_attributes(dynamodb_mock):
    event = {
        'body': '{"Weather": 25.5}'
    }
    context = {}
    expected_response = {'statusCode': 400, 'body': MSG_01}
    actual_response = lambda_handler(event, context)
    # Parse the JSON strings
    actual_response_body_parsed = json.loads(actual_response['body'])
    expected_response_body = expected_response['body']
    assert actual_response_body_parsed == expected_response_body
    assert actual_response['statusCode'] == expected_response['statusCode']

def test_extra_attributes(dynamodb_mock):
    event = {
        'body': '{"id": "123", "Weather": "High Humidity", "extra": "attribute"}'
    }
    expected_response = {'statusCode': 400, 'body': MSG_03.format(attr='extra')}
    context = {}
    actual_response = lambda_handler(event, context)
    # Parse the JSON strings
    actual_response_body_parsed = json.loads(actual_response['body'])
    expected_response_body = expected_response['body']
    assert actual_response_body_parsed == expected_response_body
    assert actual_response['statusCode'] == expected_response['statusCode']

if __name__ == '__main__':
    pytest.main()
