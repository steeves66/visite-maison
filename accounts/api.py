from ninja_extra import NinjaExtraAPI, api_controller, http_get, ControllerBase

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