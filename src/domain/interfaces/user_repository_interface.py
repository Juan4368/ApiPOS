from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
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

    @abstractmethod
    def update_user_status(
        self, user_id: int, activo: bool, actualizado_at: Optional[datetime] = None
    ) -> Optional[UserEntity]:
        """Actualiza el estado activo del usuario y devuelve la entidad actualizada."""
        raise NotImplementedError

    @abstractmethod
    def update_user(
        self,
        user_id: int,
        correo: Optional[str] = None,
        contrasena_hash: Optional[str] = None,
        role: Optional[str] = None,
        activo: Optional[bool] = None,
        nombre_completo: Optional[str] = None,
        numero_contacto: Optional[str] = None,
        actualizado_at: Optional[datetime] = None,
    ) -> Optional[UserEntity]:
        """Actualiza datos del usuario y devuelve la entidad actualizada."""
        raise NotImplementedError
