from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from oopsie.utils import response_success, response_error

@csrf_exempt
def login_view(request):
    if request.method != 'POST':
        return response_error("허용되지 않은 요청 방식입니다.", 405)
    
    try:
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")

        if not (email and password):
            return response_error("이메일과 비밀번호를 입력해 주세요.", 400)
        
        user = authenticate(request, email=email, password=password)

        if user is None:
            return response_error("이메일 또는 비밀번호가 일치하지 않습니다.", 401)
        
        login(request, user)

        return response_success({
            "data": {
                "user_id": user.id,
                "email": user.email,
                "nickname": user.nickname
            }, 
        }, "로그인 성공", 200)    
        
    except Exception as e:
        return response_error("서버오류", 500)
        