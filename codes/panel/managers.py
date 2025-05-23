from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone, password, email=None, username=None):
        if not phone:
            raise ValueError('phone is required')
        
        if not password:
            raise ValueError('password is required')
        
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            phone=phone
        )
        user.set_password(password)
        user.save(using=self._db)

        return user
    

    def create_superuser(self, phone, password, email=None, username=None):
        '''create superuser'''
        
        user = self.create_user(phone, password, email, username)

        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)

        return user