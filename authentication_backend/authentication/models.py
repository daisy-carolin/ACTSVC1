from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class UserAccountManager(BaseUserManager):
    def create_superuser(self, email, phone_number,password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        
        user =  self.create_user(email, phone_number, password, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, phone_number,password,**other_fields):
        if not email:
            raise ValueError('User must provide an Email')
            
        email = self.normalize_email(email)
        if password is not None:
            user = self.model(email=email, phone_number=phone_number,password=password, **other_fields)
            user.save()
        else:
            user = self.model(email=email, phone_number=phone_number, password=password,**other_fields)
            user.set_unusable_password()
            user.save()

        return user

class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=100, blank=False)
    phone_number= models.IntegerField(blank=False, null=True)
    otp = models.IntegerField(blank=True, null=True)
    otp_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    objects = UserAccountManager()

    def __str__(self):
        return self.email
                              