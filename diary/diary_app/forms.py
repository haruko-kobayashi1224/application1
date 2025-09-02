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
            self.add_error('password', 'パスワードが一致しません。')
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
            'username': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
            }),
        }
    
    
class PasswordChangeForm(forms.ModelForm):
    current_password = forms.CharField(
         label="現在のパスワード", 
         widget=forms.PasswordInput()
     ) 
    password = forms.CharField(
         label="新しいパスワード", 
         widget=forms.PasswordInput()
     )    
    confirm_password = forms.CharField(
         label="新しいパスワード再入力", 
         widget=forms.PasswordInput()
     )
         
    class Meta:
        model = User
        fields = ('password',)
        labels = {
            'password':'新しいパスワード',
            
        }
        widgets = {
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
            }),
        }   
    def __init__(self, *args, **kwargs):
        self.user = kwargs.get('instance')
        super().__init__(*args, **kwargs)
        
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get('current_password')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if not self.user.check_password(current_password):
            self.add_error('current_password', '現在のパスワードが間違っています。')
        if password != confirm_password:
            self.add_error('password', 'パスワードが一致しません。')
        if current_password == confirm_password:
            self.add_error('confirm_password', '前と同じパスワードにはできません。')       
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
    
       
class TodayInputForm(forms.ModelForm): 
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
        max_length=20, 
        widgets = {
           'tomorrow_goal' : forms.TextInput(
               attrs={
                #    'placeholder': '目標を書いてください（20文字以内）',
                      'class': 'form-control',},
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
        max_length=20, 
        label='その他',
        widget=forms.TextInput(
            attrs={
                # 'placeholder': 'その他にできたことを書いてください（20文字以内）',
                'class': 'form-control',                      
                              })
    )
OtherSuccessFormSet = forms.formset_factory(OtherSuccessForm, 
                                            extra=3, max_num=3, can_delete=True, validate_max=True) 


class WeekReflectionForm(forms.ModelForm):
    
    class Meta:
        model = WeekReflection
        fields = ('highlight', 'reason', 'next_plan',)
        widgets = {
           'highlight' : forms.Textarea(
               attrs={'placeholder': '例：プログラミングの勉強が2時間できた（150文字以内）',
                      'rows': 6, 
                      'cols':15},
           ),
           'reason' : forms.Textarea(
               attrs={'placeholder': '例：スキマ時間を使って学習したから（150文字以内）',
                      'rows': 6, 
                      'cols':15},
           ),
           'next_plan' : forms.Textarea(
               attrs={ 'placeholder': '例：もっと学習できるように、スマートフォンを自室に置かずに勉強をする（150文字以内）',
                       'rows': 6, 
                       'cols':15},
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
               attrs={'placeholder': '例：現実の課題に向き合えた（150文字以内）', 
                      'rows': 4, 'cols':90},
           ),
           'my_values' : forms.Textarea(
               attrs={'placeholder': '例：苦手なことでも1歩ずつ課題を達成する（150文字以内）',
                      'rows': 4, 'cols':90},
           ),
           'awareness' : forms.Textarea(
               attrs={'placeholder': '例：目の前の課題をクリアしたら、生活が充実するようになった（150文字以内）', 
                      'rows': 4, 'cols':90},
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

