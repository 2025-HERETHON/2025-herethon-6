# views.py
from django.http import JsonResponse
from django.utils.timezone import now, timedelta
from ..models import WeeklyTop3Keyword, Category
from oopsie.utils import response_error, response_success
from moments.utils.keyword_utils import save_weekly_keywords, get_weekly_keywords_data 

from django.http import JsonResponse

def get_weekly_keywords(request, category_id):
    from moments.utils.keyword_utils import save_weekly_keywords  # 필요하면 임포트
    save_weekly_keywords()
    data = get_weekly_keywords_data(category_id)
    return JsonResponse({
        'top3 키워드': data,
    })

