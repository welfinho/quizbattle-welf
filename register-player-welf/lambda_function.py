import json, boto3, uuid, time, os
dynamodb = boto3.resource("dynamodb")
table    = dynamodb.Table(os.environ["PLAYERS_TABLE"])
sns      = boto3.client("sns")
TOPIC    = os.environ["EVENT_TOPIC"]
HEADERS  = {"Access-Control-Allow-Origin": "*", "Content-Type": "application/json"}

def lambda_handler(event, _):
    data = json.loads(event.get("body", "{}"))
    name, email = data.get("name","").strip(), data.get("email","").strip()
    if not name or not email:
        return {"statusCode": 400, "headers": HEADERS, "body": json.dumps({"error":"Missing"})}

    pid = str(uuid.uuid4())
    table.put_item(Item={"playerId":pid,"name":name,"email":email,"score":0,"ts":int(time.time())})

    sns.publish(TopicArn=TOPIC, Subject="PlayerJoined",
                Message=json.dumps({"playerId":pid, "name":name, "email":email}))

    return {"statusCode":200,"headers":HEADERS,"body":json.dumps({"playerId":pid})}