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



from ninja import ModelSchema
from django.contrib.auth import get_user_model
from ninja_extra import http_post, http_delete, http_generic, route, permissions, status, http_delete, pagination
from ninja.security import APIKeyQuery
import typing
from .models import CustomUser as User
from ninja_extra.controllers.response import Detail

class UserSchemaIn(ModelSchema):
    class Config:
        model = get_user_model()
        model_fields = ['username', 'email', 'first_name', 'last_name', 'cel', 'whatsup', 'password']

class UserSchema(ModelSchema):
    class Config:
        model = get_user_model()
        model_fields = ['username', 'email', 'first_name']


@api_controller('/users')
class UsersAPIController(ControllerBase):
    user_model = get_user_model()

    @http_post()
    def create_user(self, payload: UserSchema):
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
    
    @http_generic('/{int:user_id}', methods=['put', 'patch'], response=UserSchema)
    def update_user(self, user_id: int):
        user = self.get_object_or_exception(self.user_model, id=user_id)
        return user
    
    @http_delete('/{int:user_id}', response=Detail(status_code=status.HTTP_204_NO_CONTENT))
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