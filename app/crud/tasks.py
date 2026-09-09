from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Project, Task
from app.schemas.tasks import TaskCreate, TaskUpdate


def create_task(
    db: Session,
    task_data: TaskCreate,
    owner_id: int,
) -> Task:
    project = db.get(Project, task_data.project_id)

    if project is None or project.owner_id != owner_id:
        raise ValueError("Project not found")

    task = Task(
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
        project_id=task_data.project_id,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def get_task(
    db: Session,
    task_id: int,
) -> Task | None:
    return db.get(Task, task_id)


def get_tasks(
    db: Session,
    owner_id: int,
    skip: int = 0,
    limit: int = 100,
) -> list[Task]:
    statement = (
        select(Task)
        .join(Project, Task.project_id == Project.id)
        .where(Project.owner_id == owner_id)
        .offset(skip)
        .limit(limit)
    )

    return list(db.scalars(statement).all())


def update_task(
    db: Session,
    task: Task,
    task_data: TaskUpdate,
) -> Task:
    update_data = task_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task


def delete_task(
    db: Session,
    task: Task,
) -> None:
    db.delete(task)
    db.commit()