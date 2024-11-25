module.exports.handler = async (event) => {
    const { tenant_id, order_id } = event.pathParameters;
    
    // Lógica para recuperar un pedido de DynamoDB
    return {
      statusCode: 200,
      body: JSON.stringify({ tenant_id, order_id, message: 'Order retrieved successfully' })
    };
  };
  