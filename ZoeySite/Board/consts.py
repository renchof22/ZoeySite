GAME_LIST = (
    ('Fortnite', 'Fortnite'),
    ('ApexLegends', 'ApexLegends'),
    ('CoD:BO4', 'CoD:BO4'),
    ('CoD:MW', 'CoD:MW'),
    ('BF5', 'BF5'),
    ('R6S', 'R6S'),
)

DATE_LIST = (
    (1, '今日'),
    (7, '今週'),
    (30, '今月')
)

ORDER_LIST = (
    ('-last_updated', '新着順'),
    ('last_updated', '投稿日順'),
    ('-views', 'ビューが多い順'),
    ('views', 'ビューが少ない順'),
)

from django.utils import timezone
from datetime import timedelta


def get_date_range(tmp):
    now = timezone.now()
    range = now - timedelta(days=int(tmp))
    return now, range