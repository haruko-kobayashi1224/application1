from django.db import models
from django.contrib.auth.models import(
    AbstractBaseUser, PermissionsMixin
)

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True 

class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    username = models.CharField(max_length=64)
    email =models.EmailField(max_length=128,unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    image_url = models.CharField(max_length=255, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users'
        
class UserActivateToken(models.Model):
    token = models.UUIDField(db_index=True, unique=True) 
    expired = models.DateTimeField()
    user = models.OneToOneField(
        'User',
        on_delete=models.CASCADE,
        related_name='user_activate_token',
    )  
    
    class Meta:
        db_table = 'user_activate_token'     