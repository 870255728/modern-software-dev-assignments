from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import asc, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import ActionItem, Project
from ..schemas import ProjectCreate, ProjectPatch, ProjectRead

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("/", response_model=list[ProjectRead])
def list_projects(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
) -> list[ProjectRead]:
    stmt = select(Project).order_by(asc(Project.name), asc(Project.id))
    projects = db.execute(stmt.offset(skip).limit(limit)).scalars().all()
    return [ProjectRead.model_validate(project) for project in projects]


@router.post("/", response_model=ProjectRead, status_code=201)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)) -> ProjectRead:
    project = Project(name=payload.name, description=payload.description)
    db.add(project)
    try:
        db.flush()
    except IntegrityError as error:
        raise HTTPException(
            status_code=409, detail="A project with this name already exists"
        ) from error
    db.refresh(project)
    return ProjectRead.model_validate(project)


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(project_id: int, db: Session = Depends(get_db)) -> ProjectRead:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return ProjectRead.model_validate(project)


@router.patch("/{project_id}", response_model=ProjectRead)
def patch_project(
    project_id: int,
    payload: ProjectPatch,
    db: Session = Depends(get_db),
) -> ProjectRead:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if payload.name is not None:
        project.name = payload.name
    if payload.description is not None:
        project.description = payload.description
    try:
        db.flush()
    except IntegrityError as error:
        raise HTTPException(
            status_code=409, detail="A project with this name already exists"
        ) from error
    db.refresh(project)
    return ProjectRead.model_validate(project)


@router.delete("/{project_id}", status_code=204)
def delete_project(project_id: int, db: Session = Depends(get_db)) -> Response:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    for item in db.execute(select(ActionItem).where(ActionItem.project_id == project_id)).scalars():
        item.project_id = None
    db.delete(project)
    db.flush()
    return Response(status_code=204)
