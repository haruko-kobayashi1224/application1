from django import forms 
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import Diary, WeekReflection, MonthReflection
from django.forms import modelformset_factory

User = get_user_model()

class RegistForm(forms.ModelForm):
    
    confirm_password = forms.CharField(
        label='パスワード再入力', widget=forms.PasswordInput()
    )
    
    class Meta():
        model = User
        fields = ('username', 'email', 'password')
        labels = {
            'username':'名前',
            'email':'メールアドレス',
            'password':'パスワード',
        }
        widgets = {
            'password': forms.PasswordInput()
        }
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']   
        if password != confirm_password:
            self.add_error('password', 'パスワードが一致しません')
        try: 
            validate_password(password, self.instance) 
        except ValidationError as e:
            self.add_error('password', e)
            return cleaned_data 
    
    def save(self, commit=False):
        user =super().save(commit=False) 
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user  

# class UserActivateForm(forms.Form):
#     token = forms.CharField(widget=forms.HiddenInput())
           
class LoginForm(forms.Form):
    email = forms.EmailField(label="メールアドレス")
    password = forms.CharField(label="パスワード", widget=forms.PasswordInput())    

class UserMyPageForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['user_image','username', 'email',]
        labels = {
            'user_image':'画像',
            'username':'名前',
            'email':'メールアドレス',
        }
        widgets = {
            'user_image': forms.FileInput(attrs={
                'style': 'display: none;',
                'id': 'file-upload',
            }),  
        }
    
    
class PasswordChangeForm(forms.ModelForm):
    
    confirm_password = forms.CharField(
        label='新しいパスワード再入力', widget=forms.PasswordInput()
    )
         
    class Meta:
        model = User
        fields = ('password',)
        labels ={
            'password': '新しいパスワード',
        }
        widgets = {
            'password': forms.PasswordInput()  
        }
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']   
        if password != confirm_password:
            self.add_error('password', 'パスワードが一致しません')
        try: 
            validate_password(password, self.instance) 
        except ValidationError as e:
            self.add_error('password', e)
            return cleaned_data         
                
    def save(self, commit=False):
        user =super().save(commit=False) 
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user  
    
       
class TodayInputForm(forms.ModelForm): # あなたのフォームクラス名を適切なものに置き換えてください
    diary_choices = [
        ('breakfast', '朝食が食べられた'),
        ('washing', '洗濯ができた'),
        ('throw_away', 'ごみを捨てられた'),
        ('sleep_more_than_six_hours', '6時間以上寝られた'),
        ('cooking', '自炊をした'),
    ]
    
    successes = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=diary_choices,
        required=False,
        label='今日できたこと'
    )
    
       
    class Meta:
        model = Diary
        fields =('tomorrow_goal',) 
        widgets = {
           'tomorrow_goal' : forms.Textarea(
               attrs={ 'rows': 3, 'cols':60},
           )
        }
        labels = {
           'tomorrow_goal': '',
        }          
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tomorrow_goal'].required = False
    
        
class OtherSuccessForm(forms.Form):
    other_success =forms.CharField(
        required=False,
        label='その他',
        widget=forms.Textarea(attrs={'placeholder': 'その他にできたことを書いてください',
                                     'rows': 1,
                                     'cols':40,   
                              })
    )
OtherSuccessFormSet = forms.formset_factory(OtherSuccessForm, 
                                            extra=1, max_num=3, can_delete=True, validate_max=True) 


class WeekReflectionForm(forms.ModelForm):
    
    class Meta:
        model = WeekReflection
        fields = ('highlight', 'reason', 'next_plan',)
        widgets = {
           'highlight' : forms.Textarea(
               attrs={ 'rows': 6, 'cols':15},
           ),
           'reason' : forms.Textarea(
               attrs={ 'rows': 6, 'cols':15},
           ),
           'next_plan' : forms.Textarea(
               attrs={ 'rows': 6, 'cols':20},
           )
        }
        labels = {
            'highlight':'今週のハイライト',
            'reason':'できた理由',
            'next_plan':'今後はどのような工夫をしたらよいか',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['highlight'].required = False
        self.fields['reason'].required = False
        self.fields['next_plan'].required = False

WeekReflectionFormSet = modelformset_factory(
    WeekReflection,
    form=WeekReflectionForm,
    extra=0
)    


class MonthReflectionForm(forms.ModelForm):
    class Meta:
        model = MonthReflection
        fields = ('common_ground', 'my_values', 'awareness',)
        widgets = {
           'common_ground' : forms.Textarea(
               attrs={ 'rows': 2, 'cols':70},
           ),
           'my_values' : forms.Textarea(
               attrs={ 'rows': 2, 'cols':70},
           ),
           'awareness' : forms.Textarea(
               attrs={ 'rows': 2, 'cols':70},
           )
        }
        labels = {
            'common_ground':'各週のハイライトに共通する点',
            'my_values':'自分の価値観や大切にしていること',
            'awareness':'その他気づいたこと',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['common_ground'].required = False
        self.fields['my_values'].required = False
        self.fields['awareness'].required = False

