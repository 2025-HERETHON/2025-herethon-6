from konlpy.tag import Hannanum
from collections import Counter
from django.views.decorators.csrf import csrf_exempt

sample_texts = [
    "내가 다시 취업 준비를 시작한다면 더 철저하게 할 거야.",
    "취업 면접에서 실수하지 않도록 다시 돌아간다면 준비를 더 열심히 하겠다.",
    "내가 다시 돌아간다면 이력서 작성에 더 신경 쓸 거야.",
    "취업 경쟁이 치열해서 다시 준비한다면 전략을 바꿀 거야.",
    "다시 돌아간다면 인턴 경험을 더 많이 쌓고 싶어.",
    "내가 취업 준비를 다시 한다면 자기소개서를 완벽하게 준비할 거야.",
    "다시 돌아가서 취업 박람회도 적극적으로 참여할 거야.",
    "내가 다시 돌아간다면 네트워킹에 더 힘쓸 거야.",
    "취업 준비 과정에서 부족했던 점을 보완하려고 다시 시작할 거야.",
    "다시 돌아간다면 면접관 앞에서 당황하지 않도록 연습할 거야.",
    "내가 다시 돌아간다면 직무 분석을 더 철저히 했을 거야.",
    "다시 돌아간다면 기업 분석에 더 많은 시간을 투자할 거야.",
    "내가 다시 준비한다면 자소서를 회사별로 더 맞춤화했을 거야.",
    "취업 스터디에 일찍 참여해서 정보를 나눴을 거야.",
    "다시 돌아간다면 포트폴리오를 미리미리 준비했을 거야.",
    "내가 돌아간다면 커리어 상담을 더 자주 받았을 거야.",
    "다시 돌아간다면 자격증 하나라도 더 땄을 거야.",
    "내가 다시 시작한다면 관심 기업의 인재상도 더 꼼꼼히 봤을 거야.",
    "다시 돌아간다면 취업 사이트 활용을 더 적극적으로 했을 거야.",
    "내가 다시 돌아간다면 면접 후기나 사례들을 더 많이 찾아봤을 거야."
]

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
