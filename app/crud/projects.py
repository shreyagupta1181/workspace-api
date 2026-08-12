from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Project
from app.schemas.projects import ProjectCreate, ProjectUpdate


def create_project(
    db: Session,
    project_data: ProjectCreate,
) -> Project:
    project = Project(
        name=project_data.name,
        description=project_data.description,
        owner_id=project_data.owner_id,
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project


def get_project(
    db: Session,
    project_id: int,
) -> Project | None:
    return db.get(Project, project_id)


def get_projects(
    db: Session,
    skip: int = 0,
    limit: int = 100,
) -> list[Project]:
    statement = select(Project).offset(skip).limit(limit)

    return list(db.scalars(statement).all())


def update_project(
    db: Session,
    project: Project,
    project_data: ProjectUpdate,
) -> Project:
    update_data = project_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(project, field, value)

    db.commit()
    db.refresh(project)

    return project


def delete_project(
    db: Session,
    project: Project,
) -> None:
    db.delete(project)
    db.commit()