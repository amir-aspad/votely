from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone, password, email=None, username=None, **kwargs):
        if not phone:
            raise ValueError('phone is required')
        
        if not password:
            raise ValueError('password is required')
        
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            phone=phone,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)

        return user
    

    def create_superuser(self, phone, password, email=None, username=None):
        '''create superuser'''
        return self.create_user(
            phone, password,
            email, username,
            is_admin=True, is_superuser=True
        )