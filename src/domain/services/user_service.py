from __future__ import annotations

from typing import List, Optional

from domain.dtos.userDto import UserRequest, UserResponse
from domain.entities.userEntity import UserEntity
from domain.interfaces.IUserService import IUserService
from domain.interfaces.user_repository_interface import UserRepositoryInterface


class UserService(IUserService):
    """Caso de uso para operaciones de usuarios."""

    def __init__(self, repository: UserRepositoryInterface):
        self.repository = repository

    def create_user(self, data: UserRequest) -> UserResponse:
        entity = UserEntity(
            correo=data.correo,
            contrasena_hash=data.contrasena_hash,
            role=data.role,
            activo=data.activo,
            nombre_completo=data.nombre_completo,
            creado_at=data.creado_at,
            actualizado_at=data.actualizado_at,
        )
        created = self.repository.create_user(entity)
        return UserResponse.model_validate(created)

    def list_users(self) -> List[UserResponse]:
        users = self.repository.list_users()
        return [UserResponse.model_validate(user) for user in users]

    def get_user(self, user_id: int) -> Optional[UserResponse]:
        user = self.repository.get_user(user_id)
        if not user:
            return None
        return UserResponse.model_validate(user)

    def search_users(self, term: str) -> List[UserResponse]:
        users = self.repository.search_users(term)
        return [UserResponse.model_validate(user) for user in users]
