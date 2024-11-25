module.exports.handler = async (event) => {
    const { tenant_id, product_id } = event.pathParameters;
    
    // Lógica para recuperar reseña de un producto en DynamoDB
    return {
      statusCode: 200,
      body: JSON.stringify({ tenant_id, product_id, message: 'Review retrieved successfully' })
    };
  };
  