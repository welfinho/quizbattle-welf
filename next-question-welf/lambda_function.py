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
        options = [opt["S"] for opt in question["options"]["L"]]
        correct_index = int(question["correctAnswerIndex"]["N"])
        correct_letter = ["A", "B", "C", "D"][correct_index]

        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({
                "questionId": question["questionId"]["S"],
                "questionText": question["questionText"]["S"],
                "answers": options,
                "correctAnswer": correct_letter
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }