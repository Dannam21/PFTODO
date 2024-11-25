import json
import os
import boto3
import jwt
from datetime import datetime, timedelta

dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table('Users')

SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'mysecretkey')

# Crear usuario
def create_user(event, context):
    body = json.loads(event['body'])
    tenant_id = body['tenant_id']
    user_id = body['user_id']
    email = body['email']
    
    # Insertar usuario en DynamoDB
    users_table.put_item(Item={
        'tenant_id': tenant_id,
        'user_id': user_id,
        'email': email,
        'created_at': str(datetime.now())
    })
    
    return {
        'statusCode': 201,
        'body': json.dumps({'message': 'User created successfully'})
    }

# Login usuario (genera un token JWT)
def login_user(event, context):
    body = json.loads(event['body'])
    email = body['email']
    
    # Buscar usuario por email
    response = users_table.query(
        IndexName='EmailIndex',
        KeyConditionExpression='email = :email',
        ExpressionAttributeValues={':email': email}
    )
    
    if response['Items']:
        user = response['Items'][0]
        token = jwt.encode({
            'user_id': user['user_id'],
            'tenant_id': user['tenant_id'],
            'exp': datetime.utcnow() + timedelta(hours=1)
        }, SECRET_KEY, algorithm='HS256')
        
        return {
            'statusCode': 200,
            'body': json.dumps({'token': token})
        }
    
    return {
        'statusCode': 404,
        'body': json.dumps({'message': 'User not found'})
    }

# Validar token JWT
def validate_token(event, context):
    token = event['headers'].get('Authorization')
    
    if not token:
        return {'statusCode': 403, 'body': json.dumps({'message': 'Token is missing'})}
    
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Token is valid', 'user': decoded})
        }
    except jwt.ExpiredSignatureError:
        return {'statusCode': 401, 'body': json.dumps({'message': 'Token has expired'})}
    except jwt.InvalidTokenError:
        return {'statusCode': 401, 'body': json.dumps({'message': 'Invalid token'})}
