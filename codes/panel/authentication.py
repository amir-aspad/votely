from django.contrib.auth import get_user_model

User = get_user_model()


class UsernameAuthentivate:
    def authenticate(self, request, phone=None, password=None):
        try:
            user = User.objects.get(username=phone)
            if user.check_password(password):
                return user
            return None
        
        except User.DoesNotExist:
            return None
        

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
    

class EmailAuthentivate:
    def authenticate(self, request, phone=None, password=None):
        try:
            user = User.objects.get(email=phone)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
        
