from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config import get_db
from src.domain.dtos.categoryDto import CategoryRequest, CategoryResponse
from src.domain.dtos.genericResponseDto import CreationResponse
from src.domain.services.category_service import CategoryService
from src.infrastructure.repository.createCategoryRepository import CategoryRepository

router = APIRouter(prefix="/categorias", tags=["categorias"])


def get_category_service(db: Session = Depends(get_db)) -> CategoryService:
    repo = CategoryRepository(db)
    return CategoryService(repo)


DbDep = Annotated[Session, Depends(get_db)]
ServiceDep = Annotated[CategoryService, Depends(get_category_service)]


@router.post(
    "/",
    response_model=CreationResponse[CategoryResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    payload: CategoryRequest,
    service: ServiceDep,
) -> CreationResponse[CategoryResponse]:
    try:
        created = service.create_category(payload)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return CreationResponse[CategoryResponse](id=created.categoria_id, data=created)


@router.get("/", response_model=list[CategoryResponse])
def list_categories(service: ServiceDep) -> list[CategoryResponse]:
    return service.list_categories()


@router.get("/buscar", response_model=list[CategoryResponse])
def search_categories(q: str, service: ServiceDep) -> list[CategoryResponse]:
    if not q.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El parametro q no puede estar vacio",
        )
    return service.search_categories(q.strip())


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, service: ServiceDep) -> CategoryResponse:
    categoria = service.get_category(category_id)
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoria no encontrada",
        )
    return categoria
