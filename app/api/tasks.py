from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.tasks import (
    create_task,
    delete_task,
    get_task,
    get_tasks,
    update_task,
)
from app.db.database import get_db
from app.schemas.tasks import (
    TaskCreate,
    TaskResponse,
    TaskUpdate,
)


router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task_endpoint(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
):
    return create_task(db, task_data)


@router.get(
    "/",
    response_model=list[TaskResponse],
)
def list_tasks(
    db: Session = Depends(get_db),
):
    return get_tasks(db)


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
)
def read_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    task = get_task(db, task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return task


@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
)
def update_task_endpoint(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
):
    task = get_task(db, task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return update_task(db, task, task_data)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task_endpoint(
    task_id: int,
    db: Session = Depends(get_db),
):
    task = get_task(db, task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    delete_task(db, task)