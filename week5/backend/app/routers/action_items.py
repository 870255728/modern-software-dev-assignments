from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import ActionItem
from ..schemas import ActionItemCreate, ActionItemRead, ActionItemsBulkComplete

router = APIRouter(prefix="/action-items", tags=["action_items"])


@router.get("/", response_model=list[ActionItemRead])
def list_items(
    completed: bool | None = None, db: Session = Depends(get_db)
) -> list[ActionItemRead]:
    query = select(ActionItem)
    if completed is not None:
        query = query.where(ActionItem.completed == completed)
    rows = db.execute(query).scalars().all()
    return [ActionItemRead.model_validate(row) for row in rows]


@router.post("/", response_model=ActionItemRead, status_code=201)
def create_item(payload: ActionItemCreate, db: Session = Depends(get_db)) -> ActionItemRead:
    item = ActionItem(description=payload.description, completed=False)
    db.add(item)
    db.flush()
    db.refresh(item)
    return ActionItemRead.model_validate(item)


@router.post("/bulk-complete", response_model=list[ActionItemRead])
def bulk_complete_items(
    payload: ActionItemsBulkComplete, db: Session = Depends(get_db)
) -> list[ActionItemRead]:
    rows = db.execute(select(ActionItem).where(ActionItem.id.in_(payload.ids))).scalars().all()
    items_by_id = {item.id: item for item in rows}
    missing_ids = [item_id for item_id in payload.ids if item_id not in items_by_id]

    # Validate the complete set before mutating any rows so the operation is atomic.
    if missing_ids:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "One or more action items were not found",
                "missing_ids": missing_ids,
            },
        )

    ordered_items = [items_by_id[item_id] for item_id in payload.ids]
    for item in ordered_items:
        item.completed = True

    db.flush()
    for item in ordered_items:
        db.refresh(item)
    return [ActionItemRead.model_validate(item) for item in ordered_items]


@router.put("/{item_id}/complete", response_model=ActionItemRead)
def complete_item(item_id: int, db: Session = Depends(get_db)) -> ActionItemRead:
    item = db.get(ActionItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")
    item.completed = True
    db.add(item)
    db.flush()
    db.refresh(item)
    return ActionItemRead.model_validate(item)
