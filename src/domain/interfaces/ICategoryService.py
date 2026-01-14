from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from domain.dtos.categoryDto import CategoryRequest, CategoryResponse


class ICategoryService(ABC):
    @abstractmethod
    def create_category(self, data: CategoryRequest) -> CategoryResponse:
        ...

    @abstractmethod
    def get_category(self, category_id: int) -> Optional[CategoryResponse]:
        ...

    @abstractmethod
    def list_categories(self) -> List[CategoryResponse]:
        ...

    @abstractmethod
    def search_categories(self, term: str) -> List[CategoryResponse]:
        ...
