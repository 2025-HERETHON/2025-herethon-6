from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email or not password:
            return render(request, 'login2.html', {
                'error': '이메일과 비밀번호를 입력해 주세요.'
            })

        user = authenticate(request, email=email, password=password)

        if user is None:
            return render(request, 'login2.html', {
                'error': '이메일 또는 비밀번호가 틀렸습니다.'
            })

        login(request, user)
        return redirect('/')  # 로그인 성공 시 이동할 페이지

    return render(request, 'login2.html')  # GET 요청 처리
