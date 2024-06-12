import simplejson as json
import boto3

dynamoDB = boto3.resource("dynamodb", "us-east-1")
db_routes = dynamoDB.Table("Routes")

def lambda_handler(event, context):
    print("EVENT", event)
    
    # Valida os parâmetros
    if "location_code" not in event or "route_id" not in event:
        return {
            'statusCode': 400,
            'body': "Parâmetros incorretos"
        }
    
    # Código da localização (ex.: rec)
    location_code = event["location_code"]
    # Código da rota
    route_id = event["route_id"]
    
    # Buscando item no BD
    response = db_routes.get_item(
        Key = { "PK": location_code, "SK": f"route#{route_id}" }
    )
    
    # Valida se a rota existe no BD
    if "Item" not in response:
        return {
            'statusCode': 400,
            'body': "Rota não encontrada"
        }
    
    result =  response.get("Item", {})
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': result
    }
