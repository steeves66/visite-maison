from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI

from ninja import router
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.tokens import RefreshToken
from ninja_jwt.authentication import JWTBaseAuthentication
from ninja_jwt.exceptions import TokenBackendError, TokenError
from ninja_jwt.token_blacklist.models import OutstandingToken

from ninja_extra import permissions

import pydantic
from pydantic import EmailStr, validator
from ninja import Field

api = NinjaExtraAPI()

class UserSchema(ModelSchema):
    class Config:
        model = get_user_model()
        model_fields = ['username', 'email', 'first_name', 'cel', 'last_name']
        
class UserSchemaIn(Schema):
    username: str
    email: str
    first_name: str
    last_name: str
    cel: str
    password: str
    confirm_password: str


class UserPermission(permissions.BasePermission):
    def __init__(self, request, view):
        self._permission = permission
        
    def has_permission(self, request, view):
        return request.user.has_perm(self._permisssion)


class UserPermissions(permissions.BasePermission):
    def __init__(self, request, view, *args):
        self._permissions = *args
        
    def has_permissions(self, request, view):
        for perm in *args:
            if not user.request.has_perm(perm):
                return False
        return True

@api.get("/add", tags=['Math'], auth=JWTAuth(), permissions=[permissions.IsAuthenticated() | CustomPermission()])
def add(request, a: int, b: int):
    return {"result": a + b}

@api.post('/logout', auth=JWTAuth())
def logout(request):
    try:
        token = RefreshToken(request.headers.get('refresh'))
    except TokenBackendError:
        raise TokenError(_("Token is invalid or expired"))
    token.blacklist()
    return {"access_token": str(token)}


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