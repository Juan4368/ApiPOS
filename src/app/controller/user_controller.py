from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config import get_db
from src.domain.dtos.genericResponseDto import CreationResponse
from src.domain.dtos.userDto import UserRequest, UserResponse
from src.domain.services.user_service import UserService
from src.infrastructure.repository.createUserRepository import UserRepository

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    repo = UserRepository(db)
    return UserService(repo)


DbDep = Annotated[Session, Depends(get_db)]
ServiceDep = Annotated[UserService, Depends(get_user_service)]


@router.post(
    "/",
    response_model=CreationResponse[UserResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    payload: UserRequest,
    service: ServiceDep,
) -> CreationResponse[UserResponse]:
    try:
        created = service.create_user(payload)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return CreationResponse[UserResponse](id=created.user_id, data=created)


@router.get("/", response_model=list[UserResponse])
def list_users(service: ServiceDep) -> list[UserResponse]:
    return service.list_users()


@router.get("/buscar", response_model=list[UserResponse])
def search_users(q: str, service: ServiceDep) -> list[UserResponse]:
    if not q.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El parametro q no puede estar vacio",
        )
    return service.search_users(q.strip())


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, service: ServiceDep) -> UserResponse:
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )
    return user
