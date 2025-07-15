# diary_app/utils.py
from collections import defaultdict
from .models import Diary, WeekReflection, MonthReflection
import calendar
from django.utils import timezone

def get_weeks_data(user, year, month):
    month_calendar = calendar.Calendar().monthdatescalendar(year, month)
    
    success_map = {
        'breakfast': '朝食が食べられた',
        'washing': '洗濯ができた',
        'throw_away': 'ごみを捨てられた',
        'sleep_more_than_six_hours': '6時間以上寝られた',
        'cooking': '自炊をした',
    }

    diaries = Diary.objects.filter(
        created_at__year=year,
        created_at__month=month,
        user=user
    ).order_by('created_at')
    
    try:
        month_reflection = MonthReflection.objects.get(
            user=user,
            year_number=year,
            month_number=month
        )
    except MonthReflection.DoesNotExist:
        month_reflection = None

    weeks = defaultdict(list)
    
    def get_week_number(d):
        for i, week in enumerate(month_calendar, 1):
            if d in week:
                return i
        return None

    
    for diary in diaries:
        diary_date = timezone.localtime(diary.created_at).date()
        week_num = get_week_number(diary_date)
        if not week_num :
            continue 
        
        success_list = []
        for s in diary.diarysuccess_set.all():
            s.label = success_map.get(s.success, s.success)
            success_list.append(s)
        diary.success_list = success_list
        weeks[week_num].append(diary)

    weeks_full = {}

    for week_num in range(1, 6):
        diary_list = weeks.get(week_num, [])
        week_diaries = [None] * 7
        
        
        for diary in diary_list:
            local_date = timezone.localtime(diary.created_at)
            index = local_date.weekday()  # ← ここで正しい曜日を取得
            week_diaries[index] = diary
        
        print("JST:", timezone.localtime(diary.created_at).strftime("%Y-%m-%d %H:%M:%S"))
        print("曜日:", timezone.localtime(diary.created_at).weekday())  # 0=月曜, ..., 6=日曜    
        
        
        week_reflection = None
        if month_reflection:
            week_reflection = WeekReflection.objects.filter(
                user=user,
                week_number=week_num,
                month_reflection=month_reflection
            ).first()
            
        weeks_full[week_num] = {
            "diaries": week_diaries,
            "reflection": week_reflection,
        }    

    return weeks_full
