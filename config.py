import os
from dotenv import load_dotenv

load_dotenv()

AWS_ACESS_KEY_ID = os.getenv("AWS_ACESS_KEY_ID")
AWS_SECRET_ACESS_KEY = os.getenv("AWS_SECRET_ACESS_KEY")
AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")
AWS_S3_REGION = os.getenv("AWS_S3_REGION")

