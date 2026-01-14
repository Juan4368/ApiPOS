from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config import get_db
from src.domain.dtos.genericResponseDto import CreationResponse
from src.domain.dtos.stockDto import StockRequest, StockResponse
from src.domain.services.stock_service import StockService
from src.infrastructure.repository.createStockRepository import StockRepository

router = APIRouter(prefix="/stock", tags=["stock"])


def get_stock_service(db: Session = Depends(get_db)) -> StockService:
    repo = StockRepository(db)
    return StockService(repo)


DbDep = Annotated[Session, Depends(get_db)]
ServiceDep = Annotated[StockService, Depends(get_stock_service)]


@router.post(
    "/",
    response_model=CreationResponse[StockResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_stock(
    payload: StockRequest,
    service: ServiceDep,
) -> CreationResponse[StockResponse]:
    try:
        created = service.create_stock(payload)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return CreationResponse[StockResponse](id=created.stock_id, data=created)


@router.get("/", response_model=list[StockResponse])
def list_stock(service: ServiceDep) -> list[StockResponse]:
    return service.list_stock()


@router.get("/buscar", response_model=list[StockResponse])
def search_stock(q: str, service: ServiceDep) -> list[StockResponse]:
    if not q.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El parametro q no puede estar vacio",
        )
    return service.search_stock(q.strip())


@router.get("/{stock_id}", response_model=StockResponse)
def get_stock(stock_id: int, service: ServiceDep) -> StockResponse:
    stock = service.get_stock(stock_id)
    if not stock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stock no encontrado",
        )
    return stock
