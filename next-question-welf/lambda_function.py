# lambda_function.py (for next-question-welf)
import json
import boto3
import os
import random

dynamodb = boto3.resource('dynamodb')
questions_table = dynamodb.Table(os.environ['QUESTIONS_TABLE'])

def lambda_handler(event, context):
    try:
        response = questions_table.scan()
        items = response.get("Items", [])

        if not items:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "No questions available"})
            }

        question = random.choice(items)
        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({
                "questionId": question["questionId"],
                "questionText": question["questionText"],
                "options": question["options"]
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }