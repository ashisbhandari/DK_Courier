from django.contrib.auth.backends import BaseBackend
from .models import Signup

class EmailBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            user = Signup.objects.get(email=email)
            if user.check_password(password):
                return user
        except Signup.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Signup.objects.get(pk=user_id)
        except Signup.DoesNotExist:
            return None
