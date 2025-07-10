from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now
from ..models import Moment, If, Category, Image, Moment, Category
from comments.models import Comment
from oopsie.utils import response_success, response_error
from ..image_utils import upload_to_s3, delete_from_s3
from urllib.parse import urlparse
from django.contrib.auth import get_user_model
from django.db.models import Count

User = get_user_model()

def main(request):

    # 전체 인기글 Top3
    top3_overall = Moment.objects.annotate(like_count=Count('likes'))
    
    # 각 카테고리별 인기글 Top3 딕셔너리로 저장
    categories = Category.objects.all()
    top3_by_category = {}

    for category in categories:
        moments = Moment.objects.filter(category_id=category).annotate(like_count=Count('likes')).order_by('-like_count', '-created_date')[:3]
        top3_by_category[category] = moments

    return render(request, 'moments/main.html', {
    'top3_overall': top3_overall,
    'top3_by_category': top3_by_category,})

def moment_create_view(request):
    return render(request, 'moments/moment_create.html')


def moment_list_view(request, category_id):
    # category_id를 직접 받아서 필터링
    moments = Moment.objects.filter(category_id=category_id)
    
    sort = request.GET.get('sort', 'latest')
    if sort == 'popular':
        moments = moments.annotate(like_count=Count('likes')).order_by('-like_count', '-created_date')
    else:  
        moments = moments.order_by('-created_date')
    
    return render(request, 'moment_list.html', {
        'moments': moments,
        'selected_category': category_id,  # 필요하면 이름으로 바꿔줄 수도 있음
        'sort': sort,
    })

def moment_detail_view(request, moment_id):
    moment = get_object_or_404(Moment, id=moment_id)
    images = Image.objects.filter(moment=moment)       
    comments = Comment.objects.filter(moment=moment)    
    comment_count = comments.count()

    return render(request, 'moments/moment_detail.html', {
        'moment': moment,
        'images': images,
        'comments': comments,
        'comment_count': comment_count, # 댓글수도 넘겨줌
    })

def moment_update_view(request, moment_id):
    moment = get_object_or_404(Moment, id=moment_id)
    return render(request, 'moments/moment_update.html', {'moment': moment})

'''
# 글 생성 or 목록조회 분기
@csrf_exempt
def moment_root(request): 
    if request.method == "GET":
        return moment_list(request)   
    elif request.method == "POST":
        return moment_create(request)  
    else:
        return response_error("허용되지 않은 메서드입니다", code=405)
    
# GET(글 상세조회), DELETE 기능 분기
@csrf_exempt
def moment_detail_root(request, moment_id):
    if request.method == "GET":
        return moment_detail(request, moment_id)
    elif request.method == "DELETE":
        return moment_delete(request, moment_id)
    else:
        return response_error("허용되지 않은 메서드입니다", code=405)
'''


###############################################################
# 글 생성
@csrf_exempt  
@require_http_methods(["POST"])
def moment_create(request):
    # 임시 로그인 우회 (테스트 전용)
    #from users.models import CustomUser
    #request.user = CustomUser.objects.first()  # 가장 첫 번째 유저

    if not request.user.is_authenticated:
        return response_error("로그인이 필요합니다", code=401)

    # 프론트에서 multipart/form-data로 받아와야 동작 가능하다. json만 받아오면 이미지처리 안됨
    title = request.POST.get('title')
    content = request.POST.get('content')
    if_content = request.POST.get('if_content')
    category_id = request.POST.get('category_id')
    visibility = request.POST.get('visibility', 'public') 


    # 필수 항목 검사
    if not all([title, content, if_content, category_id, visibility]):
        return response_error("필수 항목이 누락되었습니다", code=400)

    # 카테고리 존재 확인
    try:
        category_id = int(category_id)
        category = Category.objects.get(category_id=category_id)
    except (ValueError, Category.DoesNotExist):
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

        # If 생성 
        If.objects.create(
            moment_id=moment,
            if_content=if_content,
            created_date=now(),
            modified_date=now()
        )

        # 이미지 파일이 있으면 s3에 업로드
        if request.FILES.getlist('images'): # postman으로 테스트할 때 images라는 필드로 이미지 파일 업로드해야한다는 뜻
            images = request.FILES.getlist('images')
            for image_file in images:
                image_url = upload_to_s3(image_file)
                Image.objects.create(
                    moment_id=moment,
                    image_url=image_url,
                    image_name=image_file.name
                )        

        # 응답 data
        # 글 작성 후 바로 글 상세보기 페이지로 넘어가도록 프론트에서 로직을 작성했다는 전제 하의 코드임!
        data = { 
            "moment_id": moment.moment_id,
        }
        return response_success(data, message="글 작성 완료")
        

    except Exception as e:
        return response_error(f"서버 오류: {str(e)}", code=500)

###############################################################
# 글 목록조회
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
                "moment_id": moment.moment_id,
                "title": moment.title,
                "created_date": moment.created_date,
                "nickname": moment.user_id.nickname 
            })

        return response_success(result, message="글 목록 조회 성공")

    except Exception as e:
        return response_error(f"서버 오류: {str(e)}", code=500)

###############################################################
# 글 상세조회
@csrf_exempt
@require_http_methods(["GET"])
def moment_detail(request, moment_id):

    try:
        # Moment 조회 (+ user, category join)
        moment = Moment.objects.select_related('user_id', 'category_id').get(moment_id=moment_id)

        # 비공개 글인 경우
        if moment.visibility == "private" and request.user != moment.user_id:
            return response_error("비공개 글입니다", code=403)

        # 연결된 If 가져오기
        if_content = moment.if_moment.if_content  

        # 이미지들 가져오기
        images = Image.objects.filter(moment_id=moment)
        image_list = [{
            "image_id": img.image_id,
            "image_url": img.image_url,
            "image_name": img.image_name
        } for img in images]

        # 응답 데이터
        data = {
            "moment_id": moment.moment_id,
            "title": moment.title,
            "content": moment.content,
            "if_content": if_content,
            "visibility": moment.visibility,
            "category": moment.category_id.name,
            "created_date": moment.created_date,
            "modified_date": moment.modified_date,
            "user": {
                "user_id": moment.user_id.id, # CustomUser의 기본 pk인 id를 써야한다. user_id가 아니다. 
                "nickname": moment.user_id.nickname  
            },
            "images": image_list
        }

        return response_success(data, message="글 조회 성공")

    except Moment.DoesNotExist:
        return response_error("해당 글이 존재하지 않습니다", code=404)
    except Exception as e:
        return response_error(f"서버 오류: {str(e)}", code=500)

###############################################################
# 글 수정
@csrf_exempt
def moment_update(request, moment_id):
    if request.method != "POST":
        return response_error("허용되지 않은 요청 방식입니다", code=405)
    if not request.user.is_authenticated:
        return response_error("로그인이 필요합니다", code=401)

    try:
        # 수정할 글 불러오기
        moment = Moment.objects.get(moment_id=moment_id)

        # 수정 권한 체크
        if request.user != moment.user_id:
            return response_error("수정 권한이 없습니다", code=403)

        # 요청 본문 파싱 (multipart/form-data 사용 시 json으로 받으면 안 된다! -> request.POST 사용) # 이미지 때문
        title = request.POST.get('title')
        content = request.POST.get('content')
        if_content = request.POST.get('if_content')
        category_id = request.POST.get('category_id')
        visibility = request.POST.get('visibility', 'public')
        images = request.FILES.getlist('images')
        
        '''
        # 🔍 디버깅용 출력
        print("title:", title)
        print("content:", content)
        print("if_content:", if_content)
        print("category_id:", category_id)
        print("visibility:", visibility)
        print("images:", images)
'''

        # 필수값 확인
        if not all([title, content, if_content, category_id, visibility]):
            return response_error("필수 항목이 누락되었습니다", code=400)

        # 카테고리 유효성 확인
        try:
            category = Category.objects.get(category_id=category_id)
        except Category.DoesNotExist:
            return response_error("유효하지 않은 카테고리입니다", code=400)

        # Moment 수정
        moment.title = title
        moment.content = content
        moment.category_id = category
        moment.visibility = visibility
        moment.modified_date = now()
        moment.save()

        # If 내용 수정
        if_obj = If.objects.get(moment_id=moment)
        if_obj.if_content = if_content
        if_obj.save()


        # s3 이미지 처리
        if request.FILES.getlist('images'):

            # 기존 이미지 삭제 (DB + S3)
            existing_images = Image.objects.filter(moment_id=moment)
            for img in existing_images:
                parsed_url = urlparse(img.image_url)
                s3_key = parsed_url.path.lstrip('/')
                delete_from_s3(s3_key)
            existing_images.delete()

            # 새 이미지 업로드
            images = request.FILES.getlist('images')
            for image_file in images:
                image_url = upload_to_s3(image_file)
                Image.objects.create(
                    moment_id=moment,
                    image_url=image_url,
                    image_name=image_file.name
                )


        # 응답 
        data = {
            "moment_id": moment.moment_id,
            "title": moment.title,
            "modified_date": moment.modified_date
        }
        return response_success(data, message="글 수정 완료")

    except Moment.DoesNotExist:
        return response_error("글이 존재하지 않습니다", code=404)

    except If.DoesNotExist:
        return response_error("연결된 If 정보가 없습니다", code=500)

    except Exception as e:
        return response_error(f"서버 오류: {str(e)}", code=500)
    
###############################################################
# 글 삭제
@csrf_exempt
@require_http_methods(["DELETE"])
def moment_delete(request, moment_id):
    if not request.user.is_authenticated:
        return response_error("로그인이 필요합니다", code=401)
    
    try:
        moment = Moment.objects.get(moment_id=moment_id)

        if request.user != moment.user_id:
            return response_error("삭제 권한이 없습니다", code=403)

        # 연결된 이미지 먼저 삭제 (S3에서 삭제 후 DB에서 삭제하게 됨)
        images = Image.objects.filter(moment_id=moment)
        for img in images:
            parsed_url = urlparse(img.image_url)
            s3_key = parsed_url.path.lstrip('/')
            delete_from_s3(s3_key) # S3에서 삭제
            img.delete() # DB에서 삭제

        # 연결된 If 객제 삭제
        if_obj = If.objects.get(moment_id=moment)
        if_obj.delete()

        # moment 자체 삭제
        moment.delete()

        return response_success(message="글 삭제 완료")

    except Moment.DoesNotExist:
        return response_error("해당 글이 존재하지 않습니다", code=404)
    except Exception as e:
        return response_error(f"서버 오류: {str(e)}", code=500)
