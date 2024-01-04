from django.contrib.auth.models import User
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
import jwt
from datetime import datetime
from django.conf import settings


class JwtAuthentication(BaseAuthentication):
    def authenticate(self, request):
        if "Authorization" not in request.headers:
            return None

        token = request.headers["Authorization"]
        if token is None or "Bearer " not in token:
            return None

        try:
            user = self.get_user_from_token(token)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return user, None

    def get_user_from_token(self, jwt_token):
        try:
            decode_data = jwt.decode(jwt=jwt_token.replace("Bearer ", ""),
                                     key=settings.AUTH_SECRET_KEY, algorithms=settings.AUTH_ALGORITHM)
            if datetime.now() > datetime.fromtimestamp(decode_data["exp"]):
                raise Exception("Token expired")
            return User.objects.get(id=decode_data["id"])
        except Exception as e:
            message = f"Token is invalid --> {e}"
            print({"message": message})