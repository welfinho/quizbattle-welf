import json, os, boto3
dynamodb = boto3.resource("dynamodb")
table     = dynamodb.Table(os.environ["QUESTIONS_TABLE"])
HEADERS   = {"Access-Control-Allow-Origin": "*", "Content-Type": "application/json"}
ORDERED   = [f"q{i}" for i in range(1, 11)]   # q1…q10 = feste Reihenfolge

def lambda_handler(event, _):
    asked = event.get("queryStringParameters", {}).get("asked", "")
    idx   = len([x for x in asked.split(",") if x])   # 0-10
    if idx >= 10:
        return {"statusCode": 204, "headers": HEADERS, "body": ""}

    qid = ORDERED[idx]
    q   = table.get_item(Key={"questionId": qid})["Item"]
    i   = int(q["correctAnswerIndex"])

    return {"statusCode": 200, "headers": HEADERS, "body": json.dumps({
        "questionId":   qid,
        "questionText": q["questionText"],
        "answers":      q["options"],
        "correctAnswer": ["A","B","C","D"][i]
    })}