import simplejson as json
import boto3
import uuid

dynamoDB = boto3.resource("dynamodb", "us-east-1")
db_routes = dynamoDB.Table("Routes")

def lambda_handler(event, context):
    print("EVENT", event)
    
    # Valida os parâmetros
    if "location_code" not in event or "route" not in event or "route_id" not in event:
        return api_result(False, "Parâmetros incorretos")
    
    # ID da localização
    location_code = event["location_code"]
    # ID da rota
    route_id = event["route_id"]
    # Novo objeto da rota (atualizado)
    route = event["route"]
    
    updateExpression = "SET"
    expressionAttributeValues = {}
    expressionAttributeNames = {}
    
    # Itens da avaliação que vão ser atualizados
    # Aqui estamos setando dinâmicamente no formato exigido pela lib do boto3
    for r in route: 
        updateExpression += f" #{r} = :{r},"
        expressionAttributeValues[f":{r}"] = route[r]
        expressionAttributeNames[f"#{r}"] = str(r)
    
    # Removendo a última vírgula do updateExpression
    updateExpression = updateExpression[:-1]
    # print("updateExpression", updateExpression)
    # print("expressionAttributeValues", expressionAttributeValues)
    # print("expressionAttributeNames", expressionAttributeNames)
    
    # Chave primária do item do BD
    key = {
        "PK": location_code,
        "SK": f"route#{route_id}"
    }
    
    # Atualiza no BD
    response = db_routes.update_item(
        Key = key,
        UpdateExpression = updateExpression,
        ExpressionAttributeValues = expressionAttributeValues,
        ExpressionAttributeNames = expressionAttributeNames,
        ReturnValues = "ALL_NEW"
    )
    
    # Armazena resultado
    result = response.get("Attributes", {})
    
    # Sucesso
    return api_result(True, result)

# Objeto de retorno para a API
def api_result (success, body):
    return {
        'statusCode': 200 if success else 400,
        'body': body
    }
