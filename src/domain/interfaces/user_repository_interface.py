from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.userEntity import UserEntity


class UserRepositoryInterface(ABC):
    """Contrato para repositorios de usuarios en el dominio."""

    @abstractmethod
    def create_user(self, user_entity: UserEntity) -> UserEntity:
        """Persiste un usuario y devuelve la entidad creada."""
        raise NotImplementedError

    @abstractmethod
    def list_users(self) -> List[UserEntity]:
        """Devuelve todos los usuarios."""
        raise NotImplementedError

    @abstractmethod
    def get_user(self, user_id: int) -> Optional[UserEntity]:
        """Devuelve un usuario por su ID o None si no existe."""
        raise NotImplementedError

    @abstractmethod
    def search_users(self, term: str) -> List[UserEntity]:
        """Busca usuarios por correo, nombre, rol o estado."""
        raise NotImplementedError
