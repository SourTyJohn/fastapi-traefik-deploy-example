from typing import Annotated
from fastapi import Depends


DEFAULT_PAGE_SIZE = 20


class Pagination:
    def __init__(self, page: int, limit: int = DEFAULT_PAGE_SIZE) -> None:
        self._offset = (page - 1) * limit
        self._limit = limit

    @property
    def offset(self):
        return self._offset

    @property
    def limit(self):
        return self._limit


def get_pagination(
    page: int = 1,
    limit: int = DEFAULT_PAGE_SIZE,
) -> Pagination:
    return Pagination(page, limit)


PaginationDep = Annotated[Pagination, Depends(get_pagination)]
