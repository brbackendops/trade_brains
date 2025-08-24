from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):

        email = kwargs.get('email')
        try:
            user = User.objects.get(email=email)
            # print(f"User found {user.email}")
        except User.DoesNotExist:
            # print("EmailBackend: user not found")
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            # print("EmailBackend: password valid")
            return user
        else:
            # print("EmailBackend: password invalid")
            return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None