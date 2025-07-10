# views.py
from django.http import JsonResponse
from django.utils.timezone import now, timedelta
from ..models import WeeklyTop3Keyword, Category
from oopsie.utils import response_error, response_success
from moments.utils.keyword_utils import save_weekly_keywords 

def get_weekly_keywords(request, category_id):
    save_weekly_keywords()
    today = now().date()
    week_start = today - timedelta(days=today.weekday())

    try:
        category = Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        return response_error("존재하지 않는 카테고리입니다.", 404)

    try:
        weekly_data = WeeklyTop3Keyword.objects.get(week_start=week_start, category=category)
        data = weekly_data.keywords
    except WeeklyTop3Keyword.DoesNotExist:
        # 데이터가 없으면 빈 리스트 반환
        data = []

    return JsonResponse({
        '시작주': week_start.isoformat(),
        '카테고리': category.name,
        'top3 키워드': data,
    })
