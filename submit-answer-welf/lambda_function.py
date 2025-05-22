import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
players_table = dynamodb.Table(os.environ['PLAYERS_TABLE'])
questions_table = dynamodb.Table(os.environ['QUESTIONS_TABLE'])

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        player_id = body.get("playerId")
        question_id = body.get("questionId")
        answer = body.get("answer")
    except:
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": "Invalid input"})
        }

    if not player_id or not question_id or not answer:
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": "Missing fields"})
        }

    try:
        question_resp = questions_table.get_item(Key={"questionId": question_id})
        question_item = question_resp.get("Item", {})
        correct_answer = question_item.get("correctAnswer")
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": str(e)})
        }

    is_correct = (answer.strip().lower() == correct_answer.strip().lower())

    if is_correct:
        try:
            players_table.update_item(
                Key={"playerId": player_id},
                UpdateExpression="SET score = score + :inc",
                ExpressionAttributeValues={":inc": 1}
            )
        except Exception as e:
            return {
                "statusCode": 500,
                "headers": {
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"error": "Score update failed: " + str(e)})
            }

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({
            "correct": is_correct
        })
    }