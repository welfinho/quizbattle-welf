import json
import boto3
import uuid
import time
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['PLAYERS_TABLE'])

def lambda_handler(event, context):
    # Eingabe auslesen
    try:
        body = json.loads(event.get("body", "{}"))
        name = body.get("name", "").strip()
        email = body.get("email", "").strip()
    except Exception as e:
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": "Invalid input"})
        }

    # Validierung
    if not name or not email:
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": "Name and email are required"})
        }

    # Spieler-ID erzeugen
    player_id = str(uuid.uuid4())

    # Eintrag speichern
    try:
        table.put_item(Item={
            "playerId": player_id,
            "name": name,
            "email": email,
            "score": 0,
            "timestamp": int(time.time())
        })
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": str(e)})
        }

    # Erfolgreich
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({
            "playerId": player_id,
            "message": f"Willkommen, {name}!",
            "score": 0
        })
    }