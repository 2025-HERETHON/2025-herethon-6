import boto3
import uuid
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from moments.models import Image
from oopsie.utils import response_success, response_error 

@csrf_exempt
def upload_image(request):
    if request.method == "POST":
        try:
            image_file = request.FILES.get('image')
            if not image_file:
                return response_error(message="이미지가 전송되지 않았습니다.", code=400)

            # 고유 이름 생성 (중복 방지)
            unique_filename = f"{uuid.uuid4()}_{image_file.name}"

            # S3 클라이언트 생성
            s3 = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            )

            # S3에 업로드
            s3.upload_fileobj(
                image_file,
                settings.AWS_STORAGE_BUCKET_NAME,
                unique_filename,
                ExtraArgs={"ContentType": image_file.content_type}
            )

            # S3 URL 생성
            image_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{unique_filename}"

            # DB 저장
            image = Image.objects.create(
                image_url=image_url,
                image_name=image_file.name
            )

            return response_success({
                "image_id": image.image_id,
                "image_url": image.image_url,
                "image_name": image.image_name
            }, message="이미지 업로드 성공")

        except Exception as e:
            return response_error(message=f"오류 발생: {str(e)}", code=500)

    return response_error(message="POST 요청만 허용됩니다", code=405)
