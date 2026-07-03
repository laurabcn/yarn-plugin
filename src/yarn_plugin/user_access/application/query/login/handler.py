from yarn_plugin.user_access.application.query.login.query import LoginQuery
from yarn_plugin.user_access.application.query.login.response import LoginResponse
from yarn_plugin.user_access.domain.exception.invalid_credentials import InvalidCredentials
from yarn_plugin.user_access.domain.repository.user_repository_interface import UserRepositoryInterface
from yarn_plugin.user_access.infrastructure.security.jwt_service import JwtService
from yarn_plugin.user_access.infrastructure.security.password_service import PasswordService


class LoginHandler:
    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        password_service: PasswordService,
        jwt_service: JwtService,
    ) -> None:
        self._user_repository = user_repository
        self._password_service = password_service
        self._jwt_service = jwt_service

    async def handle(self, query: LoginQuery) -> LoginResponse:
        user = await self._user_repository.find_by_email(query.email)
        if user is None or not self._password_service.verify(query.password, user.password_hash):
            raise InvalidCredentials()
        token = self._jwt_service.encode(user.id, user.email)
        return LoginResponse(access_token=token)