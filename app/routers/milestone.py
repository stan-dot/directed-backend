from fastapi import Depends, HTTPException, status, Response, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import or_
from .. import models
from .. import schemas
from typing import List, Optional

router = APIRouter(
    prefix='/milestones',
    tags=["milestones"]
    )

#CRUD for milestones
@router.post(
        '/', 
        status_code=status.HTTP_201_CREATED, 
        tags=["milestones"],
        response_model=schemas.Milestone
        )
def create_milestone(milestone: schemas.Milestone, db: Session = Depends(get_db)):
    """
    creates a new milestone given a milestone object is it doesn't already exist
    returns the new milestone
    """
    old_milestone = db.query(models.Milesones).get({
        "cohort_name": milestone.cohort_name, 
        "step_nbr": milestone.step_nbr
        })
    if old_milestone:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail=f"milestone with step number: {milestone.step_nbr} in Cohort: {milestone.cohort_name} already exist, cannot create a new one with the same name.")
    new_milestone = models.Milesones(**milestone.dict())
    db.add(new_milestone)
    db.commit()
    db.refresh(new_milestone)
    return new_milestone


@router.get(
        '/', 
        response_model=List[schemas.Milestone]
        )
def get_milestones(db: Session = Depends(get_db), search:Optional[str]=""):
    """
    return all milestones for all existing cohorts
    """
    milestones = db.query(models.Milesones).filter(or_(models.Milesones.cohort_name.contains(search), models.Milesones.description.contains(search))).all()
    return milestones


@router.get(
        '/{cohort_name}:{step_nbr}', 
        response_model=schemas.Milestone
        )
def get_milestone(cohort_name: str, step_nbr: int, db: Session = Depends(get_db)):
    """
    returns milestone object by step number and cohort name
    """
    milestone = db.query(models.Milesones).get(
        {"cohort_name": cohort_name, "step_nbr": step_nbr}
        )
    if not milestone:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"milestone with step number: {step_nbr} belonging to Cohort with name: {cohort_name} not found!"
            )
    return milestone


@router.put(
        '/{cohort_name}:{step_nbr}', 
        response_model=schemas.Milestone
        )
def update_milestone(db: Session = Depends(get_db)):
    pass


@router.delete('/{cohort_name}:{step_nbr}', tags=["milestones"])
def delete_milestone(cohort_name: str, step_nbr:int, db: Session = Depends(get_db)):
    milestone = db.query(models.Milesones).filter(
        models.Milesones.cohort_name == cohort_name,
        models.Milesones.step_nbr == step_nbr
        )
    milestone.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/{cohort_name}', tags=["cohorts", "milestones"])
def get_cohort_milestones(cohort_name: str, db: Session = Depends(get_db)):
    """
    param: cohort name
    returns: all milestone objects for that cohort if exists
    """
    milestones = db.query(models.Milesones).filter(models.Milesones.cohort_name == cohort_name).order_by(models.Milesones.step_nbr).all()
    return milestones