from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Permission
from django.utils.translation import gettext_lazy as _
from django.db import models

class AccountManager(BaseUserManager):
    def create_user(self, email, username, password, first_name, **other_fields):
        if not email:
            raise ValueError(_("L'utilisateur doit avoir une adresse email"))
        if not username:
            raise ValueError(_("L'utilisateur doit avoir un nom utuilisateur"))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, first_name, password, **other_fields):
      """ other_fields.setdefault("is_staff", True)        
      other_fields.setdefault("is_superuser", True)        
      other_fields.setdefault("is_active", True)         
      other_fields.setdefault("is_admin", True)       
      if other_fields.get("is_staff") is not True:
          raise ValueError('is staff is set to False')
      if other_fields.get('is_superuser') is not True:
          raise ValueError('is_superuser is set to False')
      if other_fields.get('is_admin') is not True:
          raise ValueError('is_admin is set to False')
      return self.create_user(email, username, first_name, password, **other_fields) """
      user = self.model(
          email=email,
          username=username,
          first_name=first_name,
          is_staff=True,
          is_superuser=True,
          is_active=True,
          **other_fields
      )
      user.set_password(password)
      user.save(using=self._db)
      return user

 

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email       = models.EmailField(_('email address'), max_length=60, unique=True)
    username    = models.CharField(max_length=60, unique=True, unique=True)
    first_name  = models.CharField(max_length=60, blank=True, null=True)
    last_name   = models.CharField(max_length=60, blank=True, null=True)
    cel         = models.CharField(max_length=60, unique=True, blank=True)
    tel         = models.CharField(max_length=60, blank=True, null=True)
    whatsup     = models.CharField(max_length=60, unique=True, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    last_login  = models.DateTimeField(auto_now=True)
    is_admin    = models.BooleanField(default=False)
    is_active   = models.BooleanField(default=False)
    is_staff    = models.BooleanField(default=False)
    is_superuser= models.BooleanField(default=False)

    objects = AccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password', 'first_name']

    class Meta:
        verbose_name = ('User')
        verbose_name_plural = ('Users')

    def __str__(self):
        return self.username
 
    def get_full_name(self):
        return self.email
 
    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_staff
 
    # this methods are require to login super user from admin panel
    def has_module_perms(self, app_label):
        return self.is_staff