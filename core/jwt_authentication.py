import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from .models import Client  # Assuming the Client model is in the same app

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = self.extract_token(request)
    
        if not token:
            return None  # Return None for no authentication, not False

        try:
            payload = jwt.decode(
                token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired. Please log in again.')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token. Please log in again.')
        except:
            pass

        try:
            cliente_id = payload.get('user_id')  # Adjust based on your token field
            cliente = Client.objects.get(pk=cliente_id)  # Fetch client from database
            return (cliente, token)  # Return authenticated client and token
        except Client.DoesNotExist:
            raise AuthenticationFailed('Invalid token or user does not exist.')

    def extract_token(self, request):
        auth_header = request.headers.get('Authorization', None)

        if not auth_header:
            return None

        parts = auth_header.split()

        if len(parts) != 2:
            return None

        _, token = parts

        return token