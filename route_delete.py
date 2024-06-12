import simplejson as json
import boto3

dynamoDB = boto3.resource("dynamodb", "us-east-1")
db_routes = dynamoDB.Table("Routes")

def lambda_handler(event, context):
    print("EVENT", event)
    
    # Valida os parâmetros
    if "location_code" not in event or "route_id" not in event:
        return api_result(False, "Parâmetros incorretos")
    
    # ID da localização
    location_code = event["location_code"]
    # ID da rota
    route_id = event["route_id"]
    
    # Removendo rota do BD
    db_routes.delete_item(
        Key = {
            "PK": location_code,
            "SK": f"route#{route_id}"
        }
    )
    
    # Sucesso
    return api_result(True, f"Rota {route_id} removida com sucesso!")

# Objeto de retorno para a API
def api_result (success, body):
    return {
        'statusCode': 200 if success else 400,
        'body': body
    }
