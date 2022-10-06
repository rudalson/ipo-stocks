import boto3
import json
from custom_encoder import CustomEncoder
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb_table_name = 'ipo-stocks'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodb_table_name)


health_path = '/health'
stock_path = '/stock'
stocks_path = '/stocks'


def lambda_handler(event, context):
    logger.info(event)
    httpMethod = event['httpMethod']
    path = event['path']
    if httpMethod == 'GET' and path == health_path:
        response = build_response(200)
    elif httpMethod == 'GET' and path == stock_path:
        response = get_stock(event['queryStringParameters']['stockId'])
    elif httpMethod == 'GET' and path == stocks_path:
        response = get_stocks()
    elif httpMethod == 'POST' and path == stock_path:
        response = save_stock(json.dumps(json.loads(event['body']), ensure_ascii = False))
    elif httpMethod == 'PATCH' and path == stock_path:
        requestBody = json.loads(event['body'])
        response = modify_stock(requestBody['stockId'], requestBody['updateKey'], requestBody['updateValue'])
    elif httpMethod == 'DELETE' and path == stock_path:
        requestBody = json.loads(event['body'])
        response = delete_stock(requestBody['stockId'])

    return response


def get_stock(stock_id):
    try:
        response = table.get_item(
            Key={
                'stockId': stock_id
            }
        )
        if 'Item' in response:
            return build_response(200, response['Item'])
        else:
            return build_response(404, {'Message': 'stockId: %s not found' % stock_id})
    except:
        logger.exception('Do your custom error handling here. I am just gonna log it out here!!')


def get_stocks():
    try:
        response = table.scan()
        result = response['Items']

        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            result.extend(response['Items'])

        body = {
            'stocks': result
        }
        return build_response(200, body)
    except:
        logger.exception('Do your custom error handling here. I am just gonna log it out here!!')


def save_stock(request_body):
    try:
        table.put_item(Item=request_body)
        body = {
            'Operation': 'SAVE',
            'Message': 'SUCCESS',
            'Item': request_body
        }
        return build_response(200, body)
    except:
        logger.exception('Do your custom error handling here. I am just gonna log it out here!!')


def modify_stock(stockId, updateKey, updateValue):
    try:
        response = table.update_item(
            Key={
                'stockId': stock_id
            },
            UpdateExpression='set $s = :value' % updateKey,
            ExpressionAttributeValues={
                ':value': updateValue
            },
            ReturnValues='UPDATED_NEW'
        )
        body = {
            'Operation': 'UPDATE',
            'Message': 'SUCCESS',
            'UpdatedAttributes': response
        }
        return build_response(200, body)
    except:
        logger.exception('Do your custom error handling here. I am just gonna log it out here!!')


def delete_stock(stock_id):
    try:
        response = table.delete_item(
            Key={
                'stockId': stock_id
            },
            ReturnValues='ALL_OLD'
        )
        body = {
            'Operation': 'DELETE',
            'Message': 'SUCCESS',
            'deletedItem': response
        }
        return build_response(200, body)
    except:
        logger.exception('Do your custom error handling here. I am just gonna log it out here!!')


def build_response(status_code, body=None):
    response = {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
    if body is not None:
        response['body'] = json.dumps(body, cls=CustomEncoder)

    return response
