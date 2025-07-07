# 이미지 파일을 수정하는 경우
import boto3
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from moments.models import Image
from oopsie.utils import response_success, response_error

@csrf_exempt
def update_image(request, image_id):
    if request.method == "PUT":
        try:
            image = Image.objects.get(image_id=image_id)

            # S3에서 기존 이미지 삭제 
            s3 = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            )
            s3_key = image.image_url.split("/")[-1]
            s3.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=s3_key)

            # 수정할 새 이미지 업로드
            new_file = request.FILES.get("image")
            if not new_file:
                return response_error(message="새 이미지 파일이 필요합니다.", code=400)

            new_key = f"{image.image_id}_{new_file.name}"

            s3.upload_fileobj(
                new_file,
                settings.AWS_STORAGE_BUCKET_NAME,
                new_key,
                ExtraArgs={"ACL": "public-read"}
            )

            new_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{new_key}"

            # DB 정보 수정
            image.image_url = new_url
            image.image_name = new_file.name
            image.save()

            return response_success({
                "image_id": image.image_id,
                "image_url": image.image_url,
                "image_name": image.image_name
            }, message="이미지 파일 수정 성공")

        except Image.DoesNotExist:
            return response_error(message="이미지를 찾을 수 없습니다.", code=404)
        except Exception as e:
            return response_error(message=str(e), code=500)

    return response_error(message="PUT 요청만 허용됩니다", code=405)
