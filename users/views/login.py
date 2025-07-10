from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")

        print("📥 받은 이메일:", email)
        print("📥 받은 비밀번호:", password)

        if not (email and password):
            print("❌ 입력값 없음")
            return render(request, 'login.html', {"error": "이메일과 비밀번호를 입력해 주세요."})

        user = authenticate(request, username=email, password=password)
        print("🔎 인증된 유저:", user)

        if user is None:
            print("❌ 로그인 실패: 유저 없음")
            return render(request, 'login.html', {"error": "이메일 또는 비밀번호가 일치하지 않습니다."})

        login(request, user)
        print("✅ 로그인 성공, 리다이렉트 실행!")

        return redirect('main')
