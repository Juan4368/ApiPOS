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
        created_at = user_entity.created_at or datetime.now(timezone.utc)
        updated_at = user_entity.updated_at or created_at
        user_orm = User(
            user_id=user_entity.user_id,
            username=user_entity.username,
            email=user_entity.email,
            password_hash=user_entity.password_hash,
            thelefone_number=user_entity.thelefone_number,
            is_active=user_entity.is_active,
            is_verified=user_entity.is_verified,
            last_login_at=user_entity.last_login_at,
            created_at=created_at,
            updated_at=updated_at,
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
            User.username.ilike(like_term),
            User.email.ilike(like_term),
        ]

        lowered = term.strip().lower()
        truthy = {"true", "1", "yes", "si", "on"}
        falsy = {"false", "0", "no", "off"}
        if lowered in truthy:
            filters.append(User.is_active.is_(True))
        elif lowered in falsy:
            filters.append(User.is_active.is_(False))

        records = self.db.query(User).filter(or_(*filters)).all()
        return [UserEntity.from_model(row) for row in records]

    def update_user_status(
        self, user_id: int, is_active: bool, updated_at: Optional[datetime] = None
    ) -> Optional[UserEntity]:
        record = self.db.get(User, user_id)
        if not record:
            return None
        record.is_active = is_active
        record.updated_at = updated_at or datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(record)
        return UserEntity.from_model(record)

    def update_user(
        self,
        user_id: int,
        username: Optional[str] = None,
        email: Optional[str] = None,
        password_hash: Optional[str] = None,
        thelefone_number: Optional[str] = None,
        is_active: Optional[bool] = None,
        is_verified: Optional[bool] = None,
        last_login_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> Optional[UserEntity]:
        record = self.db.get(User, user_id)
        if not record:
            return None

        if username is not None:
            record.username = username
        if email is not None:
            record.email = email
        if password_hash is not None:
            record.password_hash = password_hash
        if thelefone_number is not None:
            record.thelefone_number = thelefone_number
        if is_active is not None:
            record.is_active = is_active
        if is_verified is not None:
            record.is_verified = is_verified
        if last_login_at is not None:
            record.last_login_at = last_login_at

        record.updated_at = updated_at or datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(record)
        return UserEntity.from_model(record)
