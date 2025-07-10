from konlpy.tag import Hannanum
from collections import Counter
from django.views.decorators.csrf import csrf_exempt

def extract_top_keywords_hannanum(texts, top_n=3):
    hannanum = Hannanum()
    all_nouns = []

    for text in texts:
        nouns = hannanum.nouns(text)
        all_nouns.extend(nouns)

    stopwords = {'시작','준비','다시','취업','내가', '더', '것', '게', '은', '는', '이', '가', '하다', '하고', '이다',
             '너무', '정말', '진짜', '그냥', '근데', '그래서', '이건', '저는', '그리고', '그때'}


    filtered = [word for word in all_nouns if word not in stopwords and len(word) > 1]
    return Counter(filtered).most_common(top_n)

from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from moments.models import If, WeeklyTop3Keyword, Category
from moments.utils.keyword_utils import extract_top_keywords_hannanum


def get_week_start_date(target_date=None):
    if target_date is None:
        target_date = datetime.today()
    start_of_week = target_date - timedelta(days=target_date.weekday())
    return start_of_week.date()



def save_weekly_keywords():
    week_start = get_week_start_date()
    start_dt = make_aware(datetime.combine(week_start, datetime.min.time()))
    end_dt = make_aware(datetime.combine(week_start + timedelta(days=6), datetime.max.time()))

    categories = Category.objects.all()

    for category in categories:
        print(f"카테고리: {category.name}")
        if_entries = If.objects.filter(
            moment_id__category_id=category.pk,
            created_date__range=(start_dt, end_dt)
        )
        print(f"해당 카테고리 IF 글 개수: {if_entries.count()}")

        texts = [entry.if_content for entry in if_entries]
        if not texts:
            print("이번 주 해당 카테고리 글이 없음")
            continue

        top_keywords = extract_top_keywords_hannanum(texts, top_n=3)
        print(f"추출된 키워드: {top_keywords}")

        keywords_only = [word for word, freq in top_keywords]

        WeeklyTop3Keyword.objects.filter(week_start=week_start, category=category).delete()
        print("기존 데이터 삭제 완료")

        entry = WeeklyTop3Keyword.objects.create(
            week_start=week_start,
            category=category,
            keywords=keywords_only
        )
        print(f"새로운 WeeklyTop3Keyword 저장됨: {entry}")

    print("주간 키워드 저장 완료")

def get_weekly_keywords_data(category_id):
    from django.utils.timezone import now
    from datetime import timedelta
    from moments.models import Category, WeeklyTop3Keyword

    today = now().date()
    week_start = today - timedelta(days=today.weekday())

    try:
        category = Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        return []

    try:
        weekly_data = WeeklyTop3Keyword.objects.get(week_start=week_start, category=category)
        data = weekly_data.keywords
    except WeeklyTop3Keyword.DoesNotExist:
        data = []

    return data
