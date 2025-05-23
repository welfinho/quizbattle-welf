# lambda_function.py (für next-question-welf)
import json
import boto3
import os
import random

dynamodb = boto3.resource('dynamodb')
questions_table = dynamodb.Table(os.environ['QUESTIONS_TABLE'])

def lambda_handler(event, context):
    try:
        # Alle Fragen abrufen
        response = questions_table.scan()
        items = response.get("Items", [])

        if not items:
            return {
                "statusCode": 404,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "body": json.dumps({"error": "No questions available"})
            }

        # Zufällige Frage wählen
        question = random.choice(items)
        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({
                "questionId": question["questionId"],
                "questionText": question["questionText"]
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": str(e)})
        }