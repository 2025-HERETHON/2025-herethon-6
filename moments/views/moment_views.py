import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.timezone import now

from ..models import Moment, If, Category
from oopsie.utils import response_success, response_error

@csrf_exempt
def moment_root(request): 
    if request.method == "GET":
        return moment_list(request)       # 글 목록 보기
    elif request.method == "POST":
        return moment_create(request)    # 글 작성
    else:
        return response_error("허용되지 않은 메서드입니다", code=405)

@csrf_exempt  
@require_http_methods(["POST"])
def moment_create(request):
    if not request.user.is_authenticated:
        return response_error("로그인이 필요합니다", code=401)
    try:
        body = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return response_error("JSON 형식이 올바르지 않습니다", code=400)

    title = body.get('title')
    content = body.get('content')  # 실패담
    if_content = body.get('if_content') # 내가 다시 돌아간다면 
    category_id = body.get('category_id')
    visibility = body.get('visibility', 'public')  

    # 필수 항목 검사
    if not all([title, content, if_content, category_id]):
        return response_error("필수 항목이 누락되었습니다", code=400)

    # 카테고리 존재 확인
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return response_error("유효하지 않은 카테고리입니다", code=400)

    try:
        # Moment 생성
        moment = Moment.objects.create(
            title=title,
            content=content,
            user_id=request.user,
            category_id=category,
            visibility=visibility,
            created_date=now(),
            modified_date=now()
        )

        # If 생성 (1:1 연결)
        If.objects.create(
            moment_id=moment,
            if_content=if_content,
            created_date=now(),
            modified_date=now()
        )

        # 응답 data
        # 글 작성 후 바로 글 상세보기 페이지로 넘어가도록 프론트에서 로직을 작성했다는 전제 하의 코드임!
        data = { 
            "moment_id": moment.id,
        }
        return response_success(data, message="글 작성 완료")

    except Exception as e:
        return response_error(f"서버 오류: {str(e)}", code=500)



@csrf_exempt
@require_http_methods(["GET"])
def moment_list(request):
    category_id = request.GET.get('category') # 쿼리파라미터로 카테고리 id 받기

    if not category_id:
        return response_error("카테고리 ID를 전달해주세요", code=400)

    try:
        # 글 목록 조회 (카테고리 필터)
        moments = Moment.objects.filter(category_id=category_id).select_related('user_id').order_by('-created_date')

        result = []
        for moment in moments:
            result.append({
                "moment_id": moment.id,
                "title": moment.title,
                "created_date": moment.created_date,
                "nickname": moment.user_id.nickname 
            })

        return response_success(result, message="글 목록 조회 성공")

    except Exception as e:
        return response_error(f"서버 오류: {str(e)}", code=500)
