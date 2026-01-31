from __future__ import annotations

from typing import List, Optional

from domain.dtos.userDto import (
    UserRequest,
    UserResponse,
    UserStatusRequest,
    UserUpdateRequest,
)
from domain.entities.userEntity import UserEntity
from domain.interfaces.IUserService import IUserService
from domain.interfaces.user_repository_interface import UserRepositoryInterface


class UserService(IUserService):
    """Caso de uso para operaciones de usuarios."""

    def __init__(self, repository: UserRepositoryInterface):
        self.repository = repository

    def create_user(self, data: UserRequest) -> UserResponse:
        entity = UserEntity(
            username=data.username,
            email=data.email,
            password_hash=data.password_hash,
            thelefone_number=data.thelefone_number,
            is_active=data.is_active,
            is_verified=data.is_verified,
            last_login_at=data.last_login_at,
            created_at=data.created_at,
            updated_at=data.updated_at,
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

    def update_user_status(
        self, user_id: int, data: UserStatusRequest
    ) -> Optional[UserResponse]:
        updated = self.repository.update_user_status(user_id, data.is_active, data.updated_at)
        if not updated:
            return None
        return UserResponse.model_validate(updated)

    def update_user(self, user_id: int, data: UserUpdateRequest) -> Optional[UserResponse]:
        updated = self.repository.update_user(
            user_id=user_id,
            username=data.username,
            email=data.email,
            password_hash=data.password_hash,
            thelefone_number=data.thelefone_number,
            is_active=data.is_active,
            is_verified=data.is_verified,
            last_login_at=data.last_login_at,
            updated_at=data.updated_at,
        )
        if not updated:
            return None
        return UserResponse.model_validate(updated)
