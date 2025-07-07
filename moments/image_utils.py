# Django 서버에서 받은 이미지 파일을 aws s3에 업로드하고 이미지 url을 반환하는 함수

import boto3
from django.conf import settings
import uuid

def upload_to_s3(file):
    # 확장자 가져오기
    extension = file.name.split('.')[-1]
    
    # 고유한 파일명 생성 (UUID 사용)
    filename = f"{uuid.uuid4()}.{extension}"
    
    # S3 클라이언트 생성
    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )

    try:
        # 파일 업로드
        s3.upload_fileobj(
            file,                      # 업로드할 파일 객체
            settings.AWS_STORAGE_BUCKET_NAME,  # S3 버킷 이름
            filename,                 # 저장할 S3 내 파일 이름
            ExtraArgs={
                'ACL': 'public-read',  # 퍼블릭으로 설정
                'ContentType': file.content_type
            }
        )

        # URL 생성
        url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/{filename}"
        return url

    except Exception as e:
        raise e
