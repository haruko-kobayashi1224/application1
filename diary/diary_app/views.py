from django.shortcuts import render, redirect, get_object_or_404
from . import forms
from django.contrib.auth.password_validation import validate_password
#from django.core.exceptions import ValidationError
#from django.contrib.auth.forms import UserCreationForm
# from .models import UserActivateToken
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required 
#from django.views import generic 
from . import mixins
from datetime import date, timedelta, datetime
#from django.forms import formset_factory
from .models import DiarySuccess, Diary, WeekReflection, MonthReflection
from .forms import RegistForm, LoginForm, UserMyPageForm, PasswordChangeForm, OtherSuccessFormSet, TodayInputForm, WeekReflectionForm, MonthReflectionForm,WeekReflectionFormSet
from django.views.generic import ListView, TemplateView
from collections import defaultdict
from django.views.decorators.http import require_POST
from django.http import Http404
from dateutil.relativedelta import relativedelta
from .utils import get_weeks_data
from django.utils import timezone
from datetime import datetime, time
from django.utils.timezone import localtime
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin


def portfolio(request):
    return render(
        request, 'portfolio.html'              
    )
    
    
def regist(request):
    regist_form = RegistForm(request.POST or None)
    today = date.today()
    if regist_form.is_valid():
       user = regist_form.save(commit=True)
       login(request, user)
       messages.success(request, 'ユーザー登録ができました！')
       return redirect('diary_app:month', year=today.year, month=today.month )
    return render(
        request, 'user/registration.html', context={
            'regist_form': regist_form,   
        }
    )
    
def user_login(request):
    login_form = LoginForm(request.POST or None)
    if login_form.is_valid():
        email = login_form.cleaned_data['email']
        password = login_form.cleaned_data['password']
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            today = date.today()
            messages.success(request, 'ログイン成功しました！')
            return redirect('diary_app:month', year=today.year, month=today.month )
        else:
            messages.warning(request, 'ログインに失敗しました')
    return render(
        request, 'user/user_login.html', context={
            'login_form': login_form,
        }              
    )    
@login_required    
def user_logout(request):    
    logout(request)    
    return redirect('diary_app:login')

  
    
@login_required
def my_page(request):
    my_page_form =UserMyPageForm(
        request.POST or None, request.FILES or None,instance=request.user
    ) 
    if my_page_form.is_valid():
        my_page_form.save()
        messages.success(request, '更新完了しました')
    return render(request, 'my_page.html',context={
        'my_page_form': my_page_form, 
        'today':date.today(), 
    })     

@login_required
def change_password(request):
    password_change_form = PasswordChangeForm(
        request.POST or None, instance=request.user
    )
    
    if password_change_form.is_valid():
        password_change_form.save(commit=True)
        update_session_auth_hash(request, request.user)
        messages.success(request, 'パスワードを変更しました')
    return render(request, 'change_password.html',context={
        'password_change_form': password_change_form,
        'today':date.today(), 
    })    
   
class MonthCalendar(LoginRequiredMixin, mixins.MonthCalendarMixin, TemplateView):
    template_name ='home.html'
            

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        
        today = timezone.localdate()
        context['today'] = today
        context['now'] = today

        diaries = Diary.objects.filter(user=self.request.user).order_by('created_at')
        diary_dates = set(localtime(d.created_at).date() for d in diaries)
        context['diary_dates'] = diary_dates
        
        dates_set = diary_dates
        streak = 0
        current = today
        
        if current not in dates_set:
            current -= timedelta(days=1)

        while current in dates_set:
            streak += 1
            current -= timedelta(days=1)


        context['streak'] =streak  
        
        diary_dict = {}
        for diary in diaries:
            date_key =localtime(diary.created_at).date().isoformat()
            diary_dict[date_key] = diary.pk
        context['diary_dict'] = diary_dict      
        
        return context

 
@login_required   
def today_input(request, year, month, day):
    naive_date = datetime(year, month, day)
    naive_datetime = datetime.combine(naive_date, time.min)
    selected_date = timezone.make_aware(naive_datetime, timezone.get_current_timezone())
    weekday = selected_date.strftime('%A')  # 英語で曜日が出る (e.g., 'Wednesday')
    weekday_jp = {'Monday': '月', 'Tuesday': '火', 'Wednesday': '水', 'Thursday': '木',
              'Friday': '金', 'Saturday': '土', 'Sunday': '日'}[weekday]
    
    diary = Diary.objects.filter(user=request.user, created_at__date=selected_date.date()).first()
    
    if request.method == 'POST':
        today_input_form = TodayInputForm(request.POST)
        formset = OtherSuccessFormSet(request.POST)   

        if today_input_form.is_valid() and formset.is_valid():
            diary = today_input_form.save(commit=False)
            diary.user = request.user
            diary.created_at = selected_date 
            diary.save()  
            
        for success in today_input_form.cleaned_data['successes']:
            DiarySuccess.objects.create(success=success, diary=diary) 
        
        for f in formset.cleaned_data:
            if f and f.get('other_success'):
                DiarySuccess.objects.create(success=f['other_success'], diary=diary)
                    
        messages.success(request, '今日の日記を作成しました')
        return redirect('diary_app:month', year=year, month=month)        
    
    else:
        today_input_form = TodayInputForm()
        formset = OtherSuccessFormSet()
        
        
    return render(
        request, 'today_input.html', context={
            'today_input_form':today_input_form,
            'year' : year,
            'month': month,
            'day':day,
            'today':date.today(), 
            'formset':formset,
            'diary': diary,
            'weekday_jp': weekday_jp
        }
    )   
    
# class DiaryInspectionListView(ListView):
#     template_name ='diary_inspection.html'
#     context_object_name = 'diaries'
    
 
#     def get_queryset(self):
#         year = self.kwargs.get('year')
#         month = self.kwargs.get('month')
#         day = self.kwargs.get('day')
        
#         user = self.request.user

#         selected_date = date(year, month, day)
#         start_datetime = timezone.make_aware(datetime.combine(selected_date, datetime.min.time()))
#         end_datetime = timezone.make_aware(datetime.combine(selected_date, datetime.max.time()))
        
#         success_map = {
#          'breakfast': '朝食が食べられた',
#          'washing': '洗濯ができた',
#          'throw_away': 'ごみを捨てられた',
#          'sleep_more_than_six_hours': '6時間以上寝られた',
#          'cooking': '自炊をした',
#          }
#         diaries = Diary.objects.filter(
#             created_at__range=(start_datetime, end_datetime),
#             user=user
#         ).order_by('-created_at')
        

        
#         for diary in diaries:
#              success_list = []
#              for s in diary.diarysuccess_set.all():
#                      s.label = success_map.get(s.success, s.success)
#                      success_list.append(s)
#              diary.success_list = success_list
             

#         return diaries

        
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         selected_date = date(
#             int(self.kwargs.get('year')),
#             int(self.kwargs.get('month')),
#             int(self.kwargs.get('day')),
#         )
        
#         context['today'] = date.today()
#         context['year'] = selected_date.year
#         context['month'] = selected_date.month
#         context['day'] = selected_date.day

        
#         context['prev_date'] = selected_date - timedelta(days=1)
#         context['next_date'] = selected_date + timedelta(days=1)
#         return context    
        
@login_required   
def edit_diary(request, pk,  year, month, day):
    diary = get_object_or_404(Diary, pk=pk)
    naive_date = datetime(year, month, day)
    naive_datetime = datetime.combine(naive_date, time.min)
    selected_date = timezone.make_aware(naive_datetime, timezone.get_current_timezone())
    weekday = selected_date.strftime('%A')  
    weekday_jp = {'Monday': '月', 'Tuesday': '火', 'Wednesday': '水', 'Thursday': '木',
              'Friday': '金', 'Saturday': '土', 'Sunday': '日'}[weekday]
    
    if diary.user.pk != request.user.pk:
        raise Http404
    if request.method == 'POST':
        edit_diary_form = TodayInputForm(request.POST, instance=diary)
        formset = OtherSuccessFormSet(request.POST)
    else:
    # 成功したチェックボックス項目だけを取得
        initial_successes = list(
            diary.diarysuccess_set
            .filter(success__in=[
                'breakfast', 'washing', 'throw_away',
                'sleep_more_than_six_hours', 'cooking'
            ])
            .values_list('success', flat=True)
        )
        edit_diary_form = TodayInputForm(instance=diary, initial={'successes': initial_successes})
    
    # 既存の自由記述を取得（チェックボックス以外）
        other_successes = diary.diarysuccess_set.exclude(success__in=[
            'breakfast', 'washing', 'throw_away', 'sleep_more_than_six_hours', 'cooking'
        ])
        formset_initial = [{'other_success': s.success} for s in other_successes]
        formset = OtherSuccessFormSet(initial=formset_initial)
    
    
    if edit_diary_form.is_valid() and formset.is_valid():
        diary = edit_diary_form.save(commit=False)
        diary.user = request.user
        diary.save()
        
       
        diary.diarysuccess_set.all().delete()
        
        for success in edit_diary_form.cleaned_data['successes']:
            DiarySuccess.objects.create(success=success, diary=diary) 
            
        for f in formset.cleaned_data:
            if f and f.get('other_success'):
                DiarySuccess.objects.create(success=f['other_success'], diary=diary)    
        
        messages.success(request, '今日の日記を更新しました')
        return redirect('diary_app:month', year=year, month=month )
        
    return render(
        request, 'edit_diary.html',context={
            'edit_diary_form': edit_diary_form,   
            'year': year,
            'month': month,
            'day': day,
            'today': date.today(),
            'formset':formset,
            'diary': diary,
            'weekday_jp': weekday_jp,
            
        }
    ) 

  
@require_POST
def delete_diary(request, pk,  year, month, day):
    diary = get_object_or_404(Diary, pk=pk, user=request.user)
    diary.delete()
    messages.success(request, '日記を削除しました')
    return redirect('diary_app:month', year=year, month=month )
      
    
    
class ReflectionListView(ListView):
    template_name ='reflection.html'
    context_object_name = 'reflections'
    
    
    def get_queryset(self):
        year = self.kwargs['year']
        month = self.kwargs['month']
    
        self.weeks = get_weeks_data(self.request.user, year, month)
        
        diaries = []
        for data in self.weeks.values():
            for diary in data['diaries']:
                if diary:
                    diaries.append(diary)
        return diaries 
    
  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = int(self.kwargs.get('year'))
        month = int(self.kwargs.get('month'))

        context['weeks'] = self.weeks 
        context['month_current'] = date(year, month, 1)
        context['month_previous'] = context['month_current'] - relativedelta(months=1)
        context['month_next'] = context['month_current'] + relativedelta(months=1)
        context['today'] = date.today()
        context['month_reflection'] = MonthReflection.objects.filter(
        user=self.request.user,
        year_number=year,
        month_number=month
        ).first()
        context['year'] = year
        context['month'] = month
        
        
        return context    
    
@login_required   
def edit_reflection(request, year, month):
    month_reflection, created =  MonthReflection.objects.get_or_create(
        user=request.user,
        year_number=year,
        month_number=month)
    
    for week_num in range(1, 6):
        WeekReflection.objects.get_or_create(
            user=request.user,
            week_number=week_num,
            month_reflection=month_reflection
    )
    
    week_queryset  = WeekReflection.objects.filter(
        user=request.user,
        month_reflection=month_reflection
    ).order_by('week_number')

    if request.method == 'POST': 
        week_formset = WeekReflectionFormSet(request.POST, queryset=week_queryset)
        month_form = MonthReflectionForm(request.POST, instance=month_reflection)
        if week_formset.is_valid() and month_form.is_valid():
            week_formset.save()
            month_form.save()
            messages.success(request, '振り返りを保存しました。')
            return redirect('diary_app:reflection', year=year, month=month)
        
    else:        
        week_formset = WeekReflectionFormSet(queryset=week_queryset)
        month_form = MonthReflectionForm(instance=month_reflection)
    
    current = date(int(year), int(month), 1)
    month_previous = current - relativedelta(months=1)
    month_next = current + relativedelta(months=1) 
    
    weeks = get_weeks_data(request.user, year, month)   
    
    week_form_pairs = list(zip(week_formset, weeks.items()))   
     
    return render(
        request, 'edit_reflection.html', context={
            'year' : year,
            'month': month,
            'today':date.today(), 
            'weeks': weeks,
            'week_formset': week_formset,
            'month_form': month_form,
            'week_form_pairs': week_form_pairs, 
            'month_previous': month_previous,
            'month_next': month_next,
            'month_reflection': month_reflection, 
        }
    )   

@require_POST
def delete_reflection(request, year, month):
    month_reflection = get_object_or_404(
        MonthReflection, 
        user=request.user,
        year_number=year,
        month_number=month)
    month_reflection.delete()
    messages.success(request, '日記を削除しました')
    return redirect('diary_app:reflection', year=year, month=month )    
    
         
    
        
        
