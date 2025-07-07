import boto3
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from moments.models import Image
from oopsie.utils import response_success, response_error

@csrf_exempt
def delete_image(request, image_id):
    if request.method == "DELETE":
        try:
            image = Image.objects.get(image_id=image_id)

            # S3에서 삭제
            s3 = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            )

            s3_key = image.image_url.split("/")[-1]
            s3.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=s3_key)

            # DB에서도 삭제
            image.delete()

            return response_success(message="이미지 삭제 성공")
        except Image.DoesNotExist:
            return response_error(message="이미지를 찾을 수 없습니다.", code=404)
        except Exception as e:
            return response_error(message=str(e), code=500)
    return response_error(message="DELETE 요청만 허용됩니다", code=405)
