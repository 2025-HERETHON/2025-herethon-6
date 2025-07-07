from django.views.decorators.csrf import csrf_exempt
from .models import Image
from oopsie.utils import response_success, response_error 
from image_utils import upload_to_s3

@csrf_exempt
def images_by_moment(request, moment_id):
    if request.method == "POST":
        try:
            images = request.FILES.getlist('images')  # 프론트에서 <input type="file" name="images" multiple>로 받아오면 됨
            result = []

            for image_file in images:
                # S3에 업로드하고 URL 받기
                image_url = upload_to_s3(image_file) 
                image = Image.objects.create(
                    moment_id=moment_id,
                    image_url=image_url,
                    image_name=image_file.name
                )
                result.append({
                    "image_id": image.id,
                    "image_url": image.image_url,
                    "image_name": image.image_name
                })

            return response_success(result, message="이미지 업로드 성공")
        except Exception as e:
            return response_error(message=str(e))

    elif request.method == "GET":
        images = Image.objects.filter(moment_id=moment_id)
        result = [{
            "image_id": img.id,
            "image_url": img.image_url,
            "image_name": img.image_name
        } for img in images]
        return response_success(result, message="이미지 조회 성공")

    elif request.method == "PUT":
        try:
            Image.objects.filter(moment_id=moment_id).delete()  # 기존 이미지 삭제하도록
            images = request.FILES.getlist('images')
            result = []

            for image_file in images:
                image_url = upload_to_s3(image_file)
                image = Image.objects.create(
                    moment_id=moment_id,
                    image_url=image_url,
                    image_name=image_file.name
                )
                result.append({
                    "image_id": image.id,
                    "image_url": image.image_url,
                    "image_name": image.image_name
                })

            return response_success(result, message="이미지 수정 완료")
        except Exception as e:
            return response_error(message=str(e))

    elif request.method == "DELETE":
        Image.objects.filter(moment_id=moment_id).delete()
        return response_success(message="이미지 삭제 완료")

    return response_error(message="허용되지 않은 메서드입니다", code=405)
