from django import forms 
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import Diary

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
        fields = ('user_image','username', 'email',)
        labels = {
            #'user_image':'画像',
            'username':'名前',
            'email':'メールアドレス',
        }
        #required = {
        #     'user_image': False,
        # }
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

# class TodayInputForm(forms.ModelForm):
        
#    class Meta:
#        model = Diary
#        fields =('tomottow_goal',) 
#        labels = {
#           'tomottow_goal': '明日の目標',
#        }    
       
class TodayInputForm(forms.ModelForm): # あなたのフォームクラス名を適切なものに置き換えてください
    diary_choices = [
        ('breakfast', '朝食が食べられた'),
        ('washing', '洗濯ができた'),
        ('throw_away', 'ごみを捨てられた'),
        ('sleep_more_than_six_hours', '6時間以上寝られた'),
        ('cooking', '自炊をした'),
        # 他の選択肢があればここに追加
    ]
    
    successes = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=diary_choices,
        required=False,
        label='今日できたこと'
    )
    

        
    # 今日できたこと = forms.MultipleChoiceField(
    #     widget=forms.CheckboxSelectMultiple,
    #     choices=diary_choices,
    # )        
    class Meta:
        model = Diary
        fields =('tomorrow_goal',) 
        widgets = {
           'tomorrow_goal' : forms.Textarea(
               attrs={ 'rows': 5, 'cols':60},
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
        widget=forms.TextInput(attrs={'placeholder': 'その他にできたことを書いてください'})
    )
OtherSuccessFormSet = forms.formset_factory(OtherSuccessForm, 
                                            extra=1, max_num=3, can_delete=True, validate_max=True)    



    
      