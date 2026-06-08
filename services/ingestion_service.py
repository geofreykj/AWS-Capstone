import boto3
from utils.pdf_parser import extract_pdf_text

session = boto3.Session(profile_name="capstone")

s3_client = session.client("s3")

def get_file_bytes(bucket_name, key):
    response = s3_client.get_object(
        Bucket=bucket_name,
        Key=key
    )

    return response["Body"].read()


def extract_markdown_text(file_bytes):
    return file_bytes.decode("utf-8")


def extract_text(filename, file_bytes):

    if filename.lower().endswith(".pdf"):
        return extract_pdf_text(file_bytes)

    if filename.lower().endswith(".md"):
        return extract_markdown_text(file_bytes)

    raise Exception("Unsupported file type")