import simplejson as json
import boto3

dynamoDB = boto3.resource("dynamodb", "us-east-1")
db_routes = dynamoDB.Table("Routes")

def lambda_handler(event, context):
    print("EVENT", event)
    
    # Valida os parâmetros
    if "location_code" not in event:
        return api_result(False, "Parâmetros incorretos")
    
    # Código da localição (ex.: rec) 
    location_code = event["location_code"]
    
    # Listando rotas
    response = db_routes.query(
        KeyConditionExpression = "PK = :PK AND begins_with(SK, :SK)",
        ExpressionAttributeValues = { ":PK": location_code, ":SK": "route#"}
    )
    
    # Se a lista não for encontrada ou estiver vazia
    # Lembrando que o DB sempre retorna o atributo "Items" mesmo que esteja vazio
    if not response["Items"]:
        return api_result(False, "Nenhuma rota encontrada")
    
    result =  response.get("Items", [])
    
    # TODO implement
    return api_result(True, result)

# Objeto de retorno para a API
def api_result (success, body):
    return {
        'statusCode': 200 if success else 400,
        'body': body
    }
