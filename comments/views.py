import json
from django.views.decorators.csrf import csrf_exempt
from comments.models import Comment
from moments.models import Moment
from oopsie.utils import response_success, response_error
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.shortcuts import redirect

User = get_user_model()

# POST, GET 메서드 분기
@csrf_exempt
def comment_root(request, moment_id):
    if request.method == 'GET':
        return comment_list(request, moment_id)
    elif request.method == 'POST':
        return comment_create(request, moment_id)
    else:
        return response_error("허용되지 않은 메서드입니다", code=405)
    
# PUT, DELETE 메서드 분기
@csrf_exempt
def comment_detail_root(request, moment_id, comment_id):
    if request.method == 'POST': 
        return comment_update(request, moment_id, comment_id)
    elif request.method == 'DELETE':
        return comment_delete(request, moment_id, comment_id)
    else:
        return response_error("허용되지 않은 메서드입니다", code=405)
    

####################################################
# 댓글 생성 (POST)

@csrf_exempt
def comment_create(request, moment_id):
    # 임시 로그인 우회 (테스트 전용)
    #from users.models import CustomUser
    #request.user = CustomUser.objects.first()  # 가장 첫 번째 유저

    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    try:
        # 게시글 유효성 검사
        try:
            moment = Moment.objects.get(moment_id=moment_id)
        except Moment.DoesNotExist:
            return response_error("해당 게시글이 존재하지 않습니다", code=404)

        # JSON 파싱
        body = json.loads(request.body)
        user_id = body.get('user_id')
        content = body.get('content')

        if not content:
            return redirect('moment_detail_view', moment_id=moment_id)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return response_error("사용자가 존재하지 않습니다", code=404)

        # 댓글 저장
        Comment.objects.create(
            moment_id=moment,
            user_id=user,
            content=content
        )

        return redirect('moment_detail_view', moment_id=moment_id)

    except json.JSONDecodeError:
        return response_error("JSON 형식이 올바르지 않습니다", code=400)

    except Exception as e:
        return response_error(f"서버 오류: {str(e)}", code=500)


# 특정 게시글의 댓글 목록 조회 (GET)
def comment_list(request, moment_id):
    try:
        # moment_id에 해당하는 게시글이 존재하는지 확인
        moment = Moment.objects.get(moment_id=moment_id)

        # 해당 게시글의 댓글 모두 조회 (최신순)
        comments = Comment.objects.filter(moment_id=moment).order_by('-created_date')

        # 댓글 리스트 직렬화
        comment_data = [
            {
                "comment_id": comment.comment_id,
                "user_nickname": comment.user_id.nickname,
                "content": comment.content,
                "created_date": comment.created_date,
                "modified_date": comment.modified_date
            }
            for comment in comments
        ]

        return redirect('moment_detail_view', moment_id=moment_id)

    except Moment.DoesNotExist:
        return response_error("해당 게시글이 존재하지 않습니다", code=404)

    except Exception as e:
        return response_error(f"서버 오류: {str(e)}", code=500)
    

# 댓글 수정 (POST)
@csrf_exempt
def comment_update(request, moment_id, comment_id):
    user = request.user
    if not user.is_authenticated:
        return response_error("로그인이 필요합니다", code=401)
    if comment.user_id != request.user:
        return response_error("댓글 수정 권한이 없습니다", code=403)
    
    try:
        # JSON 파싱
        body = json.loads(request.body)
        user_id = body.get('user_id')
        content = body.get('content')

        if not user_id or not content:
            return response_error("user_id와 content는 필수입니다", code=400)

        # 게시글 존재 확인
        try:
            moment = Moment.objects.get(moment_id=moment_id)
        except Moment.DoesNotExist:
            return response_error("해당 게시글이 존재하지 않습니다", code=404)

        # 댓글 존재 확인 + 게시글 연결 체크
        try:
            comment = Comment.objects.get(comment_id=comment_id, moment_id=moment)
        except Comment.DoesNotExist:
            return response_error("해당 댓글이 존재하지 않거나 게시글과 일치하지 않습니다", code=404)

        # 사용자 권한 확인
        if str(comment.user_id.id) != str(user_id):
            return response_error("댓글 수정 권한이 없습니다", code=403)

        # 수정
        comment.content = content
        comment.modified_date = now()
        comment.save()

        return redirect('moment_detail_view', moment_id=comment.moment_id.moment_id)

    except json.JSONDecodeError:
        return response_error("JSON 형식이 올바르지 않습니다", code=400)

    except Exception as e:
        return response_error(f"서버 오류: {str(e)}", code=500)
    

# 댓글 삭제 (DELETE)
@csrf_exempt
def comment_delete(request, moment_id, comment_id):
    user = request.user
    if not user.is_authenticated:
        return response_error("로그인이 필요합니다", code=401)
    if request.method != 'DELETE':
        return response_error("DELETE 요청만 허용됩니다", code=405)
    if comment.user_id != request.user:
        return response_error("댓글 삭제 권한이 없습니다", code=403)

    try:
        # JSON 파싱
        body = json.loads(request.body)
        user_id = body.get('user_id')

        if not user_id:
            return response_error("user_id는 필수입니다", code=400)

        # 게시글 존재 확인
        try:
            moment = Moment.objects.get(moment_id=moment_id)
        except Moment.DoesNotExist:
            return response_error("해당 게시글이 존재하지 않습니다", code=404)

        # 댓글 존재 + 게시글 일치 확인
        try:
            comment = Comment.objects.get(comment_id=comment_id, moment_id=moment)
        except Comment.DoesNotExist:
            return response_error("해당 댓글이 존재하지 않거나 게시글과 일치하지 않습니다", code=404)

        # 권한 확인
        if str(comment.user_id.id) != str(user_id):
            return response_error("댓글 삭제 권한이 없습니다", code=403)

        # 삭제
        comment.delete()

        return redirect('moment_list_view', moment_id=moment_id)

    except json.JSONDecodeError:
        return response_error("JSON 형식이 올바르지 않습니다", code=400)

    except Exception as e:
        return response_error(f"서버 오류: {str(e)}", code=500)