from fastapi import Depends, HTTPException, status, Response, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models
from .. import schemas
from typing import List

router=APIRouter(
    prefix='/cohorts',
    tags=["cohorts"]
    )

#CRUD for cohorts
@router.post(
        '/', 
        status_code=status.HTTP_201_CREATED, 
        response_model=schemas.Cohort
        )
def create_cohort(cohort: schemas.Cohort, db: Session = Depends(get_db)):
    """
    creates a new cohort given a cohort object is it doesn't already exist
    returns the new cohort
    """
    old_cohort = db.query(models.Cohorts).get(ident=cohort.name)
    if old_cohort:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"cohort with name: {cohort.name} already exist, cannot create a new one with the same name.")
    new_cohort = models.Cohorts(**cohort.dict())
    db.add(new_cohort)
    db.commit()
    db.refresh(new_cohort)
    return new_cohort


@router.get(
        '/', 
        response_model=List[schemas.Cohort]
        )
def get_cohorts(db: Session = Depends(get_db)):
    """
    returns all cohort objects
    """
    cohorts = db.query(models.Cohorts).all()
    return cohorts

@router.get(
        '/{cohort_name}',
        response_model = schemas.Cohort
        )
def get_cohort(cohort_name: str, db: Session = Depends(get_db)):
    """
    returns cohort object by name
    """
    cohort = db.query(models.Cohorts).filter(models.Cohorts.name==cohort_name).first()
    if not cohort:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"cohort with name: {cohort_name} not found!"
            )
    return cohort


@router.put(
        '/{cohort_name}', 
        response_model=schemas.Cohort
        )
def update_cohort(cohort_name: str, updated_cohort: schemas.Cohort, db: Session = Depends(get_db)):
    cohort_query = db.query(models.Cohorts).filter(models.Cohorts.name==cohort_name)
    cohort = cohort_query.first()
    if not cohort:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The cohort with name {cohort_name} doesn't exist")
    cohort_query.update(updated_cohort.dict(), synchronize_session=False)
    db.commit()
    return cohort_query.first()


@router.delete('/{cohort_name}')
def delete_cohort(cohort_name:str, db: Session = Depends(get_db)):
    milestones = db.query(models.Milesones).filter(models.Milesones.cohort_name == cohort_name)
    cohort = db.query(models.Cohorts).filter(models.Cohorts.name == cohort_name)
    milestones.delete(synchronize_session=False)
    cohort.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.get(
        '/{cohort_name}/students', 
        tags=["cohorts", "students"],
        response_model=List[schemas.Student]
        )
def get_students_from_cohort(cohort_name: str, db: Session = Depends(get_db)):
    """
    param: cohort name
    returns: all student objects enrolled in given cohort if exists
    """
    students = db.query(models.Students).filter(models.Students.cohort == cohort_name).order_by(models.Students.name).all()
    return students
