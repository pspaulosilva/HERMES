import simplejson as json
import boto3
import uuid

dynamoDB = boto3.resource("dynamodb", "us-east-1")
db_routes = dynamoDB.Table("Routes")

def lambda_handler(event, context):
    print("EVENT", event)
    
    # Valida os parâmetros
    if "location_code" not in event or "route" not in event:
        return {
            'statusCode': 400,
            'body': "Parâmetros incorretos"
        }
    
    # Código da localização (ex.: rec)
    location_code = event["location_code"]
    # Objeto da rota
    route = event["route"]
    
    # Criando ID da nova rota
    route_id = str(uuid.uuid4())
    
    # Inicializando objeto de criação da rota
    # Aqui adicionamos os atributos de reviews e tags com contadores zerados
    data = {
        "PK": f"{location_code}",
        "SK": f"route#{route_id}",
        "reviews": {
          "average": 0,
          "total": 0
         },
         "tags": {
          "bathroom_quality": 0,
          "clean": 0,
          "secure": 0,
          "street_condition": 0,
          "water_access": 0
         }
    }
    
    # Atualizando rota, adicionando o objeto que vem do front
    data.update(route)

    # Criando rota no BD
    db_routes.put_item(
        Item = data
    )
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': f"Rota {route_id} criada com sucesso."
    }
