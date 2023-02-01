from rest_framework.authtoken.models import Token
from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
 
 
@database_sync_to_async
def returnUser(token_string):
    try:
       
        print("midd")
        print(token_string)
        access_token_obj = RefreshToken(token_string, verify=True)
        u=access_token_obj['username']
        print(u)
        print("hmmmm")
        user=User.objects.get(username=u)
    except:
        user = AnonymousUser()
    return user
 
 
class TokenAuthMiddleWare:
    def __init__(self, app):
        self.app = app
 
    async def __call__(self, scope, receive, send):
        query_string = scope["query_string"]
        query_params = query_string.decode()
        query_dict = parse_qs(query_params)
        token = query_dict["token"][0]

        print(token)
        user = await returnUser(token)
        print(user)
        scope["user"] = user
        return await self.app(scope, receive, send)