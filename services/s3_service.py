import boto3

BUCKET_NAME = "rag-capstone-jeff"

session = boto3.Session(profile_name="capstone")

s3_client = session.client("s3")

def upload_file(uploaded_file):
    key = f"documents/{uploaded_file.name}"

    s3_client.upload_fileobj(
        uploaded_file,
        BUCKET_NAME,
        
        key
    )

    return key