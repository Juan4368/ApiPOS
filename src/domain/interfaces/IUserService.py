from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from domain.dtos.userDto import (
    UserRequest,
    UserResponse,
    UserStatusRequest,
    UserUpdateRequest,
)


class IUserService(ABC):
    @abstractmethod
    def create_user(self, data: UserRequest) -> UserResponse:
        ...

    @abstractmethod
    def get_user(self, user_id: int) -> Optional[UserResponse]:
        ...

    @abstractmethod
    def list_users(self) -> List[UserResponse]:
        ...

    @abstractmethod
    def search_users(self, term: str) -> List[UserResponse]:
        ...

    @abstractmethod
    def update_user_status(self, user_id: int, data: UserStatusRequest) -> Optional[UserResponse]:
        ...

    @abstractmethod
    def update_user(self, user_id: int, data: UserUpdateRequest) -> Optional[UserResponse]:
        ...
