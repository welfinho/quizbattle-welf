import json, os, boto3
dynamodb = boto3.resource("dynamodb")
players   = dynamodb.Table(os.environ["PLAYERS_TABLE"])
questions = dynamodb.Table(os.environ["QUESTIONS_TABLE"])
sns       = boto3.client("sns")
TOPIC     = os.environ["EVENT_TOPIC"]
HEADERS   = {"Access-Control-Allow-Origin": "*", "Content-Type": "application/json"}

def lambda_handler(event, _):
    body = json.loads(event.get("body", "{}"))
    pid  = body.get("playerId")
    score = body.get("score")          # gesendet beim Finish

    # === Finish-Fall – Score mailen =========================
    if score is not None:
        email = players.get_item(Key={"playerId": pid})["Item"]["email"]
        sns.publish(
            TopicArn = TOPIC,
            Subject  = "QuizFinished",
            Message  = json.dumps({"email": email, "score": score})
        )
        return {"statusCode": 200, "headers": HEADERS, "body": "{}"}

    # === Normaler Antwort-Fall ==============================
    qid   = body.get("questionId")
    ans   = body.get("answer", "").strip().upper()
    qitem = questions.get_item(Key={"questionId": qid})["Item"]
    correct = ["A","B","C","D"][int(qitem["correctAnswerIndex"])]
    ok = ans == correct
    if ok:
        players.update_item(
            Key={"playerId": pid},
            UpdateExpression="ADD score :inc",
            ExpressionAttributeValues={":inc": 1}
        )
    return {"statusCode": 200, "headers": HEADERS,
            "body": json.dumps({"correct": ok})}