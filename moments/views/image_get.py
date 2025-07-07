from django.views.decorators.csrf import csrf_exempt
from moments.models import Image
from oopsie.utils import response_success, response_error

@csrf_exempt
# 특정 게시글의 이미지 조회하는 경우
def get_images_by_moment(request, moment_id):
    if request.method == "GET":
        try:
            images = Image.objects.filter(moment_id=moment_id).values("image_id", "image_url", "image_name")
            return response_success(list(images), message="이미지 조회 성공")
        except Exception as e:
            return response_error(message=str(e))
    return response_error(message="GET 요청만 허용됩니다", code=405)

# 이미지 전체 조회 (쓸 일이 있을진 모르겠음)
def get_images(request):
    if request.method == "GET":
        try:
            images = Image.objects.all().values("image_id", "image_url", "image_name")
            return response_success(list(images), message="이미지 전체 조회 성공")
        except Exception as e:
            return response_error(message=str(e))
    return response_error(message="GET 요청만 허용됩니다", code=405)
