from sqlalchemy import or_
from sqlalchemy.orm import Query


def paginate(query: Query, page: int, page_size: int) -> tuple[list, int]:
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return items, total


def apply_sort(
    query: Query,
    model,
    sort_column: str | None,
    allowed_columns: set[str],
    order: str = "asc",
) -> Query:
    if not sort_column or sort_column not in allowed_columns:
        return query
    column = getattr(model, sort_column)
    return query.order_by(column.desc() if order == "desc" else column.asc())


def apply_search(
    query: Query, model, search: str | None, search_columns: list[str]
) -> Query:
    if not search:
        return query
    conditions = [getattr(model, col).ilike(f"%{search}%") for col in search_columns]
    return query.filter(or_(*conditions))
