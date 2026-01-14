from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config import get_db
from src.domain.dtos.genericResponseDto import CreationResponse
from src.domain.dtos.productsDto import ProductRequest, ProductResponse
from src.domain.services.product_service import ProductService
from src.infrastructure.repository.createProductsRepository import ProductRepository

router = APIRouter(prefix="/productos", tags=["productos"])


def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    repo = ProductRepository(db)
    return ProductService(repo)


DbDep = Annotated[Session, Depends(get_db)]
ServiceDep = Annotated[ProductService, Depends(get_product_service)]


@router.post(
    "/",
    response_model=CreationResponse[ProductResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    payload: ProductRequest,
    service: ServiceDep,
) -> CreationResponse[ProductResponse]:
    try:
        created = service.create_product(payload)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc

    return CreationResponse[ProductResponse](id=created.producto_id, data=created)


@router.get("/", response_model=list[ProductResponse])
def list_products(service: ServiceDep) -> list[ProductResponse]:
    return service.list_products()


@router.get("/buscar", response_model=list[ProductResponse])
def search_products(q: str, service: ServiceDep) -> list[ProductResponse]:
    if not q.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El parametro q no puede estar vacio",
        )
    return service.search_products(q.strip())


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, service: ServiceDep) -> ProductResponse:
    producto = service.get_product(product_id)
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado",
        )
    return producto
