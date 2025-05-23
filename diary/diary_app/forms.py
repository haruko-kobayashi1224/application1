from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class UserForm(forms.ModelForm):
    
    confirm_password = forms.CharField(
        label='パスワード再入力', widget=forms.PasswordInput()
    )
    
    class Meta():
        model = User
        fields = ('username', 'email', 'password')
        labels = {
            'username': '名前',
            'email':'メールアドレス',
            'password':'パスワード',
        }
        widgets = {
            'password': forms.PasswordInput()
        }
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        confirm_password = cleaned_data['password']   
        if password != confirm_password:
            self.add_error('password', 'パスワードが一致しました')
        try: 
            validate_password(password, self.instance) 
        except ValueError as e:
            self.add_error('password', e)
            return cleaned_data  