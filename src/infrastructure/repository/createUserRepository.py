from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from domain.entities.userEntity import UserEntity
from domain.interfaces.user_repository_interface import UserRepositoryInterface
from src.infrastructure.models.models import User


class UserRepository(UserRepositoryInterface):
    """Repositorio para manejar operaciones relacionadas con usuarios."""

    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_entity: UserEntity) -> UserEntity:
        creado_at = user_entity.creado_at or datetime.now(timezone.utc)
        actualizado_at = user_entity.actualizado_at or creado_at
        user_orm = User(
            user_id=user_entity.user_id,
            correo=user_entity.correo,
            contrasena_hash=user_entity.contrasena_hash,
            role=user_entity.role,
            activo=user_entity.activo,
            creado_at=creado_at,
            actualizado_at=actualizado_at,
            nombre_completo=user_entity.nombre_completo,
        )

        self.db.add(user_orm)
        self.db.commit()
        self.db.refresh(user_orm)
        return UserEntity.from_model(user_orm)

    def list_users(self) -> List[UserEntity]:
        records = self.db.query(User).all()
        return [UserEntity.from_model(row) for row in records]

    def get_user(self, user_id: int) -> Optional[UserEntity]:
        record = self.db.get(User, user_id)
        if not record:
            return None
        return UserEntity.from_model(record)

    def search_users(self, term: str) -> List[UserEntity]:
        like_term = f"%{term}%"
        filters = [
            User.correo.ilike(like_term),
            User.nombre_completo.ilike(like_term),
            User.role.ilike(like_term),
        ]

        lowered = term.strip().lower()
        truthy = {"true", "1", "yes", "si", "on"}
        falsy = {"false", "0", "no", "off"}
        if lowered in truthy:
            filters.append(User.activo.is_(True))
        elif lowered in falsy:
            filters.append(User.activo.is_(False))

        records = self.db.query(User).filter(or_(*filters)).all()
        return [UserEntity.from_model(row) for row in records]
