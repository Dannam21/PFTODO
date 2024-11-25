import json
import boto3

dynamodb = boto3.resource('dynamodb')
categoria_table = dynamodb.Table('Categoria')

def create_categoria(event, context):
    body = json.loads(event['body'])
    tenant_id = body['tenant_id']
    category_id = body['category_id']
    
    # Crear categoría en DynamoDB
    categoria_table.put_item(Item={
        'tenant_id': tenant_id,
        'category_id': category_id,
        'name': body['name']
    })
    
    return {
        'statusCode': 201,
        'body': json.dumps({'message': 'Category created successfully'})
    }
