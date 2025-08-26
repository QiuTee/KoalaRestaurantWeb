from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _ 
from django.contrib.auth.models import  Group
class UserManager(BaseUserManager):
    use_in_migrations = True
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError :
            raise ValueError(_("Please enter a valid email address"))

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email,first_name, last_name , password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        else:
            email = self.normalize_email(email)
            self.email_validator(email)
        if not first_name:
            raise ValueError(_('The first name must be set'))
        if not last_name:
            raise ValueError(_('The last name must be set'))
        user = self.model(email=email,first_name = first_name,last_name = last_name,  **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('group', Group.objects.get(name='admin'))
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self._create_user(email, password, **extra_fields)
    

class CustomerManager(BaseUserManager): 
    use_in_migrations = True
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError :
            raise ValueError(_("Please enter a valid email address"))
    
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        else:
            email = self.normalize_email(email)
            self.email_validator(email)
        
        user = self.model(email=email , **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    
class ManagerManager(BaseUserManager): 
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        else:
            email = self.normalize_email(email)
            self.email_validator(email)
        
        user = self.model(email=email , **extra_fields)
        user.set_password(password)
        user.save()
        return user

