import boto3
from botocore.exceptions import ClientError
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_S3_REGION, AWS_S3_BUCKET

s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_S3_REGION
)

def check_s3(s3):
    try:
        s3.head_bucket(Bucket=AWS_S3_BUCKET)
        print("S3 está online e funcional")
    except ClientError as e:
        print("Erro ao conectar ao S3:", e)

def upload_file(file_path, key):
    s3.upload_file(file_path, AWS_S3_BUCKET, key)
    return f"https://{AWS_S3_BUCKET}.s3.{AWS_S3_REGION}.amazonaws.com/{key}"