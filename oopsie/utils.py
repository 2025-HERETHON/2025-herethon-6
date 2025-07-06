# 응답 통일

from django.http import JsonResponse

def response_success(data=None, message="성공", code=200):
    return JsonResponse({
        "code": code,
        "message": message,
        "data": data or {}
    }, status=code)

def response_error(message="실패", code=400):
    return JsonResponse({
        "code": code,
        "message": message,
        "data": {}
    }, status=code)
