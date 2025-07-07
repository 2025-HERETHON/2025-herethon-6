# Django 서버에서 받은 이미지 파일을 aws s3에 업로드하고 이미지 url을 반환하는 함수

import boto3
from django.conf import settings
import uuid

## S3에 파일 업로드하는 함수
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
                'ContentType': file.content_type
            }
        )

        # URL 생성
        url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{filename}"
        return url

    except Exception as e:
        raise e

## S3에서부터 파일 하나만 지울 때 쓰는 함수
def delete_from_s3(filename):
    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )

    try:
        s3.delete_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=filename  # 매개변수로 받은 key값. s3 내의 파일 경로.
        )
    except Exception as e:
        raise e
