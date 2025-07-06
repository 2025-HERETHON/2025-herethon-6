from django.shortcuts import render
from django.http import JsonResponse
import json
from users.models import CustomUser
from django.db import IntegrityError
from oopsie.utils import response_error, response_success
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def signup(request):
    if request.method != 'POST':
        return response_error("허용되지 않은 요청 방식입니다.", 405)
    
    try:
        data = json.loads(request.body)
        email = data.get("email")
        nickname = data.get("nickname")
        password = data.get("password")

        if not (email and nickname and password):
            return response_error("모든 값을 입력해 주세요.", 400)
        
        user = CustomUser.objects.create_user(email=email, nickname=nickname, password=password)

        return response_success(
            {"user_id":user.id, "email":user.email, "nickname":user.nickname},
            "회원가입 성공",
            201
        )
    
    # 정책 준수
    except ValueError as e:
        return response_error(str(e), 400)
    
    # DB 중복
    except IntegrityError:
        return response_error("이미 존재하는 이메일 또는 닉네임입니다.",409)
        
    
    # JSON 파싱 실패
    except json.JSONDecodeError:
        return response_error("요청 형식이 올바르지 않습니다.", 400)
    
    # 서버 오류
    except Exception as e:
        return response_error("서버 오류", 500)
    
    