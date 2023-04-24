from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI

from ninja import router
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.tokens import RefreshToken
from ninja_jwt.authentication import JWTBaseAuthentication
from ninja_jwt.exceptions import TokenBackendError, TokenError
from ninja_jwt.token_blacklist.models import OutstandingToken
api = NinjaExtraAPI()

@api.get("/add", tags=['Math'], auth=JWTAuth())
def add(request, a: int, b: int):
    return {"result": a + b}

@api.post('/logout', auth=JWTAuth())
def logout(request):
    token = RefreshToken(request.headers.get('refresh'))
    try:
        access_token = token.access_token
    except TokenBackendError:
        raise TokenError(_("Token is invalid or expired"))
    
    if access_token is None:
        token.blacklist()
        print("deleted**************************" + str(token))
        return {"access_token": str(token)}
    else:
        token.blacklist()
        print("deleted**************************" + str(token))
        jti = access_token.__getitem__('jti')
        
        """ out_token = OutstandingToken.objects.get(jti=str(access_token))
        out_token.delete() """
        
        return {"refresh_token": str(token),
                "access_token": str(access_token), 
                "jit": str(jti)}


@api.get('/get_token')
def get_token(request):
    pass
    # print(request.user.last_name)
    #print(request.data)


@api.get('/get_token_old', auth=JWTAuth())
def get_token(request):
    # JWT_authentication = JWTBaseAuthentication()
    """  headers = request
    print(headers.user.is_authenticated()) """
    # print("Yes**************************")
    """ if headers.__contains__("Authorization"):
        header = request.headers.get('Authorization')
    else:
        header = "there is no Authorization headers" """
    """ for k, v in headers:
        print(k, v) """
    # print(request.META)
    # return {'header': dict(header)}

    meta = request.headers
    for k, v in meta.items():
         print(k, v)
    
    print(request.user.email)

    # return {'header': dict(meta)}

    # print(request.user.auth)

    """     if request.user.is_authenticated():
        print("Yes****************")
        return {"is_authenticated": "Yes"}
    else:
        print('No **********************')
        return {"is_authenticated": "No"} """


api.register_controllers(NinjaJWTDefaultController)