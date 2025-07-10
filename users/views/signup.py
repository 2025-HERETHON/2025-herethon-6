from django.shortcuts import render
from django.http import JsonResponse
import json
from users.models import CustomUser
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.http import HttpResponseRedirect

@csrf_exempt
def signup_view(request):
    if request.method == 'GET':
        return render(request, 'signup.html')


    elif request.method == 'POST':
        email = request.POST.get("email")
        nickname = request.POST.get("nickname")
        password = request.POST.get("password")

        if not (email and nickname and password):
            return render(request, 'signup.html', {"error": "모든 값을 입력해 주세요."})

        try:
            user = CustomUser.objects.create_user(email=email, nickname=nickname, password=password)
            return redirect('/main/')  
        except ValueError as e:
            return render(request, 'signup.html', {"error": str(e)})
        except IntegrityError:
            return render(request, 'signup.html', {"error": "이미 존재하는 이메일 또는 닉네임입니다."})
        except Exception as e:
            return render(request, 'signup.html', {"error": "서버 오류"})

    else:
        return render(request, 'signup.html', {"error": "허용되지 않은 요청 방식입니다."})
