from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
# from .models import UserActivateToken
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required 
from django.views import generic 
from . import mixins
from datetime import date, timedelta, datetime
from django.forms import formset_factory
from .models import DiarySuccess, Diary
from .forms import RegistForm, LoginForm, UserMyPageForm, PasswordChangeForm, OtherSuccessFormSet, TodayInputForm
from django.views.generic import ListView


def portfolio(request):
    return render(
        request, 'portfolio.html'              
    )
    
    
def regist(request):
    regist_form = RegistForm(request.POST or None)
    today = date.today()
    if regist_form.is_valid():
       regist_form.save(commit=True)
       return redirect('diary_app:month', year=today.year, month=today.month )
    return render(
        request, 'user/registration.html', context={
            'regist_form': regist_form,   
        }
    )
# def activate_user(request, token):
#     activate_form = forms.UserActivateForm(request.POST or None)
#     if activate_form.is_valid():
#         UserActivateToken.objects.activate_user_by_token(token) #ユーザーを有効化
#         messages.success(request,'ユーザーを有効化しました')
#     activate_form.initial['token'] = token
#     return render(
#         request, 'user/activate_user.html', context={
#             'activate_form': activate_form,
#         }
#     )  
    
def user_login(request):
    login_form = LoginForm(request.POST or None)
    if login_form.is_valid():
        email = login_form.cleaned_data['email']
        password = login_form.cleaned_data['password']
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            today = date.today()
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
    return redirect('diary_app:user_login')
    #     password =user_form.cleaned_data.get('password', '')
    #     try:
    #         validate_password(password)
    #     except ValidationError as e:
    #        user_form.add_error('password', e)
    #     user.set_password(password)
    #     user.save()
    # user_form = UserCreationForm(request.POST or None)  
    # if user_form.is_valid(): 
    #     user_form.save()

class DiaryInspectionListView(ListView):
    queryset = Diary.objects.all()
    template_name ='diary_inspection.html'
    context_object_name = 'diaries'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['today'] = date.today() 
    #     return context 

    
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')

        selected_date = date(year, month, day)
        start_datetime = datetime.combine(selected_date, datetime.min.time())
        end_datetime = datetime.combine(selected_date, datetime.max.time())
        
        success_map = {
        'breakfast': '朝食が食べられた',
        'washing': '洗濯ができた',
        'throw_away': 'ごみを捨てられた',
        'sleep_more_than_six_hours': '6時間以上寝られた',
        'cooking': '自炊をした',
        }
        diaries = Diary.objects.filter(
        created_at__range=(start_datetime, end_datetime)
        ).order_by('-created_at')

        
        for diary in diaries:
            success_list = []
            for s in diary.diarysuccess_set.all():
                    s.label = success_map.get(s.success, s.success)
                    success_list.append(s)
            diary.success_list = success_list

        return diaries

        # return Diary.objects.filter(
        #     created_at__range=(start_datetime, end_datetime)
        # ).order_by('-created_at')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_date = date(
            self.kwargs.get('year'),
            self.kwargs.get('month'),
            self.kwargs.get('day'),
        )
        context['today'] = date.today()
        context['year'] = selected_date.year
        context['month'] = selected_date.month
        context['day'] = selected_date.day

        # 前日・翌日を計算して渡す
        context['prev_date'] = selected_date - timedelta(days=1)
        context['next_date'] = selected_date + timedelta(days=1)
        return context    
        # date_str = self.request.GET.get('date')
        # if date_str:
        #     try:
        #         selected_date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
        #     except ValueError:
        #         selected_date = timezone.localdate()
        # else:
        #     selected_date = timezone.localdate()

        # # その日付のDiaryだけに絞る
        # start_datetime = timezone.datetime.combine(selected_date, timezone.datetime.min.time())
        # end_datetime = timezone.datetime.combine(selected_date, timezone.datetime.max.time())
        # qs = Diary.objects.filter(created_at__range=(start_datetime, end_datetime)).order_by('-created_at')
        # return qs
        # qs = super().get_queryset()
        # return qs  

# def diary_inspection(request):
#     today = date.today()
#     diary = Diary.objects.fetch_all_inspection()
#     return render(
#         request, 'diary_inspection.html',context={
#             'today':date.today(), 
#             'diary':diary,
#         }
#     )          

def reflection(request):
    
    return render(
        request, 'reflection.html',context={
            'today':date.today(), 
            
        }
    )   

    
# def my_page(request):
#     return render(
#         request, 'my_page.html'
    # ) 
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
        messages.success(request, 'パスワードを変更しました')
        return redirect('diary_app:login') 
    return render(request, 'change_password.html',context={
        'password_change_form': password_change_form,
        'today':date.today(), 
    })    
   
class MonthCalendar(mixins.MonthCalendarMixin, generic.TemplateView):
    template_name ='home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        context['today'] = date.today() 
        return context

# def home(request):
#     return render(
#         request, 'home.html' 
#     )       
#できたことを入力する 
@login_required   
def today_input(request, year, month, day):
    # selected_date = date(year, month, day)
    if request.method == 'POST':
        today_input_form = TodayInputForm(request.POST)
        formset = OtherSuccessFormSet(request.POST)   

        if today_input_form.is_valid() and formset.is_valid():
            diary = today_input_form.save(commit=False)
            diary.user = request.user
            # form.instance.date = selected_date
            diary.save()  
            
        for success in today_input_form.cleaned_data['successes']:
                DiarySuccess.objects.create(success=success, diary=diary) 
        
        # for f in formset.cleaned_data:
        #         if f and f.get('other_success'):
        #             DiarySuccess.objects.create(success=f['other_success'], diary=diary)
                    
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
        }
    )   