from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self,email,password=None,**kwargs):
        if not email:
            raise ValueError("Users must have a valid email address.")
        account=self.model(email=self.normalize_email(email),**kwargs)
        account.set_password(password)
        account.save(using=self._db)
        return account
    def create_superuser(self,email,password,**kwargs):
        account=self.create_user(email=email,password=password,**kwargs)
        
        account.is_staff = True
        account.is_superuser = True
        account.is_active = True
        account.save(using=self._db)
        return account

