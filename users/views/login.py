from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login

@csrf_exempt
def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not (email and password):
            return render(request, 'login.html', {"error": "이메일과 비밀번호를 입력해 주세요."})

        user = authenticate(request, username=email, password=password)

        if user is None:
            return render(request, 'login.html', {"error": "이메일 또는 비밀번호가 일치하지 않습니다."})

        login(request, user)
        return redirect('/main/')