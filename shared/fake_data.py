import boto3
import random
import string

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Users')

def generate_fake_data(tenant_id, num_items):
    for _ in range(num_items):
        user_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        email = f'user{user_id}@example.com'
        table.put_item(Item={
            'tenant_id': tenant_id,
            'user_id': user_id,
            'email': email,
            'created_at': '2024-11-24'
        })

for tenant_id in ['tenant1', 'tenant2', 'tenant3']:
    generate_fake_data(tenant_id, 10000)
