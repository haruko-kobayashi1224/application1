from django.db import models
from django.contrib.auth.models import(
    BaseUserManager,AbstractBaseUser, PermissionsMixin
)
from django.db.models.signals import post_save
from django.dispatch import receiver
from uuid import uuid4
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import UserManager


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True 
        
class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('メールアドレスは必須です')  
        if not username:
            raise ValueError('ユーザー名は必須です')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields) 
        user.set_password(password)  
        user.save()
        return user
    
    def create_superuser(self, email, username, password=None, **extra_fields):  
         extra_fields['is_staff'] = True
         extra_fields['is_active'] = True
         extra_fields['is_superuser'] = True
         return self.create_user(email, username, password, **extra_fields)
         

class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    username = models.CharField(max_length=64)
    email =models.EmailField(max_length=128,unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    user_image = models.FileField(upload_to='user_images',null=True, blank=True)   
     
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email

    class Meta:
        db_table = 'users'

# class UserActivateTokenManager(models.Manager):
    
#     def activate_user_by_token(self, token):
#         user_activate_token =self.filter(
#             token=token,
#             expired_at__gte=timezone.now()
#         ).first()
#         if not user_activate_token:
#             raise ValueError('トークンが存在しません')
        
#         user = user_activate_token.user
#         user.is_active = True
#         user.save()
#         return user
        
        
#     def create_or_update_token(self, user):  
#         token =str(uuid4()) #トークンの発行      
#         expired_at = timezone.now() + timedelta(days=1) #トークンの期限（1日後）
#         user_token, created = self.update_or_create(
#             user=user,
#             defaults={'token': token, 'expired_at': expired_at,}
#         )
#         return user_token
        
# class UserActivateToken(models.Model):
#     token = models.UUIDField(db_index=True, unique=True) 
#     expired_at = models.DateTimeField()
#     user = models.OneToOneField(
#         'User',
#         on_delete=models.CASCADE,
#         related_name='user_activate_token',
#     )  
    
#     objects: UserActivateTokenManager = UserActivateTokenManager()
    
#     class Meta:
#         db_table = 'user_activate_token'   

# @receiver(post_save, sender=User)
# def publish_token(sender, instance, created, **kwargs):        
#     user_activate_token =UserActivateToken.objects.create_or_update_token(instance)
#     print(
#         f'http://127.0.0.1:8000/diary_app/activate_user/{user_activate_token.token}'
#     )     

# class DiaryManager(models.Manager):
#     def fetch_all_inspection(self):
#         return self.order_by('id').all()    


class Diary(TimeStampedModel):
    tomorrow_goal = models.CharField(max_length=50,null=True, blank=True)  
    user = models.ForeignKey(
        'User',on_delete=models.CASCADE,
    ) 
    week_reflection = models.ForeignKey(
        'WeekReflection',on_delete=models.CASCADE,null=True, blank=True
    ) 
    
    @property
    def weekday_index(self):
        return self.created_at.weekday()
    
    class Meta:
        db_table = 'diaries'
        
    
# objects: DiaryManager = DiaryManager()    

class DiarySuccess(TimeStampedModel):
    success = models.CharField(max_length=50) 
    diary = models.ForeignKey(
        'Diary',on_delete=models.CASCADE,
    ) 
      
    
    class Meta:
        db_table = 'diary_successes'

class WeekReflection(TimeStampedModel):
    week_number = models.IntegerField()
    highlight = models.CharField(max_length=50,null=True, blank=True)
    reason = models.CharField(max_length=50,null=True, blank=True)
    next_plan = models.CharField(max_length=50,null=True, blank=True)   
    user = models.ForeignKey(
        'User',on_delete=models.CASCADE,   
    )  
    month_reflection = models.ForeignKey(
        'MonthReflection',on_delete=models.CASCADE,
    ) 
   
    class Meta:
        db_table = 'week_reflections'         
        
class MonthReflection(TimeStampedModel):
    year_number = models.IntegerField()
    month_number = models.IntegerField()
    common_ground = models.CharField(max_length=50,null=True, blank=True)
    my_values = models.CharField(max_length=50,null=True, blank=True)
    awareness = models.CharField(max_length=50,null=True, blank=True)   
    user = models.ForeignKey(
        'User',on_delete=models.CASCADE,
    ) 
    
    class Meta:
        db_table = 'month_reflections' 
        
       
        
        

             
            