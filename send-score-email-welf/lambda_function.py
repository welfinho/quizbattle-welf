import json, os, boto3
ses   = boto3.client("ses")
SENDER = os.environ["SENDER"]

def lambda_handler(event, _):
    msg   = json.loads(event["Records"][0]["Sns"]["Message"])
    score = msg["score"]; email = msg.get("email")  # optional lookup
    if not email: return
    ses.send_email(
        Source=SENDER,
        Destination={"ToAddresses":[email]},
        Message={
          "Subject":{"Data":"Dein Quiz-Ergebnis"},
          "Body":{"Text":{"Data":f"Du hast {score}/10 Punkten erreicht. Glückwunsch!"}}
        })
