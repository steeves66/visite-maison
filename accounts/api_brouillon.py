""" """ from ninja_extra import api_controller, route, NinjaExtraAPI
from ninja import constants
from ninja_jwt.controller import TokenObtainPairController, NinjaJWTDefaultController

api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)

user = get_model_user()

@api_controller('', tags=['My Operations'], auth=constants.NOT_SET, permissions=[])
class UserAPIController:
    @route.get('/users/{user_id}')
    def get_user_by_id(self, user_id:int):
        return {'user_id': user_id}
    
    @route.get('/users')
    def get_users(self):
        pass

api.register_controllers(MyCustomController)



from ninja_extra import api_controller, route
from ninja_jwt.authentication import JWTAuth

@api_controller()
class MyController:
    @route.get('/some-endpoint', auth=JWTAuth())
    def some_endpoint(self):
        pass
    

from ninja import router
from ninja_jwt.authentication import JWTAuth

router = router('')
@router.get('/some-endpoint', auth=JWTAuth())
def some_endpoint(self):
    pass




###
from ninja_extra import NinjaExtraAPI, api_controller, http_get

api = NinjaExtraAPI()

# function based definition
@api.get("/add", tags=['Math'])
def add(request, a: int, b: int):
    return {"result": a + b}

#class based definition
@api_controller('/', tags=['Math'], permissions=[])
class MathAPI:

    @http_get('/subtract',)
    def subtract(self, a: int, b: int):
        """Subtracts a from b"""
        return {"result": a - b}

    @http_get('/divide',)
    def divide(self, a: int, b: int):
        """Divides a by b"""
        return {"result": a / b}

    @http_get('/multiple',)
    def multiple(self, a: int, b: int):
        """Multiples a with b"""
        return {"result": a * b}

api.register_controllers(
    MathAPI
)

...
from django.urls import path
from .api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),  # <---------- !
]

###




#------------------------------------------------------------------------------------------------- ControllerBase
import uuid
from ninja import ModelSchema
from ninja_extra import (
    http_get, http_post, http_generic, http_delete,
    api_controller, status, ControllerBase, pagination
)
from ninja_extra.controllers.response import Detail
from django.contrib.auth import get_user_model


class UserSchema(ModelSchema):
    class Config:
        model = get_user_model()
        model_fields = ['username', 'email', 'first_name']


@api_controller('/users')
class UsersController(ControllerBase):
    user_model = get_user_model()

    @http_post()
    def create_user(self, user: UserSchema):
        # just simulating created user
        return self.Id(uuid.uuid4())

    @http_generic('/{int:user_id}', methods=['put', 'patch'], response=UserSchema)
    def update_user(self, user_id: int):
        """ Django Ninja will serialize Django ORM model to schema provided as `response`"""
        user = self.get_object_or_exception(self.user_model, id=user_id)
        return user

    @http_delete('/{int:user_id}', response=Detail(status_code=status.HTTP_204_NO_CONTENT))
    def delete_user(self, user_id: int):
        user = self.get_object_or_exception(self.user_model, id=user_id)
        user.delete()
        return self.create_response('', status_code=status.HTTP_204_NO_CONTENT)

    @http_get("", response=pagination.PaginatedResponseSchema[UserSchema])
    @pagination.paginate(pagination.PageNumberPaginationExtra, page_size=50)
    def list_user(self):
        return self.user_model.objects.all()

    @http_get('/{user_id}', response=UserSchema)
    def get_user_by_id(self, user_id: int):
        user = self.get_object_or_exception(self.user_model, id=user_id)
        return user
    
    
    router = Router()

    @router.post('/login')
    def login(request, username: str, password: str):
        user = authenticate(request, username=username, password=password)
        if user is not None:
            jwt = JSONWebToken.create(user)
            return {'token': jwt.access_token}
        else:
            return {'error': 'Invalid credentials'}
#----------------------------------------------------------------------------------------------APIController Route Decorator
from ninja_extra import route, api_controller
from ninja_extra.controllers import RouteFunction

@api_controller
class MyController:
    @route.get('/test')
    def test(self):
        return {'message': 'test'}

assert isinstance(MyController.test, RouteFunction) # true




# -------------------------------------------------------- from drf rest api with pyJWT
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
import jwt, datetime


# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response


class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response """






 """
 
 # *********************************************************** *********************
 
 from ninja_extra import NinjaExtraAPI, api_controller, http_get, ControllerBase

from ninja import router
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.tokens import RefreshToken
from ninja_jwt.authentication import JWTBaseAuthentication
from ninja_jwt.exceptions import TokenBackendError, TokenError
from ninja_jwt.token_blacklist.models import OutstandingToken
api = NinjaExtraAPI()

@api.get("/add")
def add(request, a:int, b:int):
    return {'result': a+b}

@api_controller('/', tags=['Math'], permissions=[])
class MathAPI:

    @http_get('/substract')
    def substract(self, a: int, b: int):
        """Substract a from b"""
        return {"result": a - b}
    
    @http_get('/divide')
    def divide(self, a: int, b: int):
        """Divide a by b"""
        return {"result": a / b}
    
    @http_get('/multiply')
    def multiply(self, a: int, b:int):
        """Multiply a by b"""
        return {"result": a * b}

api.register_controllers(MathAPI)



from ninja import ModelSchema, Schema
from django.contrib.auth import get_user_model
from ninja_extra import http_post, http_delete, http_generic, route, permissions, status, http_delete, pagination
from ninja.security import APIKeyQuery
import typing
from .models import CustomUser as User
from ninja_extra.controllers.response import Detail
from pydantic import BaseModel, ValidationError, validator

# class UserSchemaIn(ModelSchema):
#     class Config:
#         model = get_user_model()
#         model_fields = ['username', 'email', 'first_name', 'last_name', 'cel', 'whatsup', 'password']


class UserSchemaIn(Schema):
    username: str
    email: str
    first_name: str
    last_name: str
    cel: str
    whatsup: str
    password1: str
    password2: str

    @validator('name')
    def name_must_contain_space(cls, v):
        if ' ' not in v:
            raise ValueError('must contain a space')
        return v.title()

    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):
        if 'password1' in values and v != values['password1']:
            raise ValueError('passwords do not match')
        return v


class UserSchema(ModelSchema):
    class Config:
        model = get_user_model()
        model_fields = ['username', 'email', 'first_name', 'cel', 'email', 'last_name', 'whatsup']
        
        

@api.get("/add-users", tags=['Another_Users'], response=UserSchema)
def add(request, payload: UserSchemaIn):
    return {payload}

@api.post('/logout', auth=JWTAuth())
def logout(request):
    try:
        token = RefreshToken(request.headers.get('refresh'))
    except TokenBackendError:
        raise TokenError(_("Token is invalid or expired"))
    token.blacklist()
    return {"access_token": str(token)}

@api.get('/get_token')
def get_token(request):
    pass
    # print(request.user.last_name)
    #print(request.data)

@api_controller('/users')
class UsersAPIController(ControllerBase):
    user_model = get_user_model()

    @http_post(response=UserSchema)
    def create_user(self, payload: UserSchemaIn):
        new_user = User.objects.create(
            username=payload.username,
            email=payload.email,
            first_name=payload.first_name,
            last_name=payload.last_name,
            cel=payload.cel,
            whatsup=payload.whatsup,
        )
        new_user.set_password(payload.password)
        new_user.save()
        return new_user
    
    @http_generic('/{int:user_id}/update', methods=['put', 'patch'], response=UserSchema)
    def update_user(self, user_id: int, payload: UserSchema):
        user = self.get_object_or_exception(self.user_model, id=user_id)
        user.username=payload.username
        user.first_name=payload.first_name
        user.last_name=payload.last_name
        user.cel=payload.cel
        user.whatsup=payload.whatsup
        user.save()
        return user
    
    @http_delete('/{int:user_id}/delete', response=Detail(status_code=status.HTTP_204_NO_CONTENT))
    def delete_user(self, user_id:int):
        user = self.get_object_or_exception(self.user_model, id=user_id)
        user.delete()
        return self.create_response('', status_code=status.HTTP_204_NO_CONTENT)

    @http_get('', response=pagination.PaginatedResponseSchema[UserSchema])
    @pagination.paginate(pagination.PageNumberPaginationExtra, page_size=50)
    def list_user(self):
        return self.user_model.objects.all()
    
    @http_get('/{user_id}', response=UserSchema)
    def get_user_by_id(self, user_id: int):
        user = self.get_object_or_exception(self.user_model, id=user_id)
        return user



""" @api_controller('/users', auth=[APIKeyQuery()] tags=['Users'], permissions=[permissions.IsAuthenticated])
class UserAPI(ControllerBase):
    user_model = get_user_model()

    @http_post()
    def create_user(self, user: UserSchema):
        # just simulating created user

    @http_generic('/{int: user_id}', methods=['put', 'patch'], response=UserSchema) """


""" @api_controller('users/')
class UsersAPI(ControllerBase):
    @route.get('', response={200: typing.List[UserSchema]})
    def get_users(self):
        users = User.objects.all()
        return users

    @route.post('create/', response={200: UserSchema})
    def create_user(self, payload: UserSchemaIn):
        # Logic to handle POST request to the /users endpoint
        new_user = User.objects.create(
            username=payload.username,
            email=payload.email,
            first_name=payload.first_name,
            last_name=payload.last_name,
            cel=payload.cel,
            whatsup=payload.whatsup,
        )
        new_user.set_password(payload.password)
        new_user.save()
        return new_user
 """
api.register_controllers(UsersAPIController)