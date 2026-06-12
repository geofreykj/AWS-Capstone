import json
import boto3
from dotenv import load_dotenv
import os

# bedrock = boto3.client(
#     "bedrock-runtime",
#     region_name="us-east-1"
# )

# session = boto3.Session(profile_name="capstone")

MODEL_ID = os.getenv("MODEL_ID")

# s3 = session.client("s3")

# bedrock = session.client(
#     "bedrock-runtime",
#     region_name="us-east-1"
# )

s3 = boto3.client("s3")

bedrock = boto3.client(
    "bedrock-runtime",
    region_name="us-east-1"
)


def get_embedding(text):

    response = bedrock.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=json.dumps({
            "inputText": text
        })
    )

    response_body = json.loads(
        response["body"].read()
    )

    return response_body["embedding"]

def generate_answer(question, context):
    prompt = f"""
You are a helpful RAG assistant.

Answer ONLY using the provided context.
If the answer is not present in the context, say:
"I could not find that information in the uploaded documents."

Context:
{context}

Question:
{question}
"""

    response = bedrock.converse(
        modelId=MODEL_ID,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        inferenceConfig={
            "maxTokens": 1024,
            "temperature": 0.2
        }
    )
    print(response)
    return response["output"]["message"]["content"][0]["text"]