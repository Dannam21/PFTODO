import json
import boto3

dynamodb = boto3.resource('dynamodb')
producto_table = dynamodb.Table('Producto')

def create_producto(event, context):
    body = json.loads(event['body'])
    tenant_id = body['tenant_id']
    product_id = body['product_id']
    
    # Crear producto en DynamoDB
    producto_table.put_item(Item={
        'tenant_id': tenant_id,
        'product_id': product_id,
        'name': body['name'],
        'price': body['price']
    })
    
    return {
        'statusCode': 201,
        'body': json.dumps({'message': 'Product created successfully'})
    }
