from fastapi import Depends, HTTPException, status, Response, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models
from .. import schemas
from typing import List

router = APIRouter(
    prefix='/schools',
    tags=["schools"]
    )

#CRUD for schools
@router.post(
        '/', 
        status_code=status.HTTP_201_CREATED,
        response_model=schemas.School
        )
def create_school(school: schemas.School, db: Session = Depends(get_db)):
    """
    creates a new school given a school object is it doesn't already exist
    returns the new school
    """
    old_school = db.query(models.Schools).get(ident=school.name)
    if old_school:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"school with name: {school.name} already exist, cannot create a new one with the same name.")
    new_school = models.Schools(**school.dict())
    db.add(new_school)
    db.commit()
    db.refresh(new_school)
    return new_school

@router.get(
        '/', 
        response_model=List[schemas.School]
        )
def get_schools(db: Session = Depends(get_db)):
    """
    returns all school objects
    """
    schools = db.query(models.Schools).all()
    return schools


@router.get(
        '/{school_name}', 
        response_model=schemas.School
        )
def get_school(school_name: str, db: Session = Depends(get_db)):
    """
    returns school object by name
    """
    school = db.query(models.Schools).filter(models.Schools.name == school_name).first()
    if not school:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"school with name: {school_name} not found!"
            )
    return school


@router.put('/{school_name}', tags=["schools"])
def update_school(db: Session = Depends(get_db)):
    pass

@router.delete(
        '/{school_name}', 
        status_code=status.HTTP_204_NO_CONTENT
        )
def delete_school(school_name: str, db: Session = Depends(get_db)):
    school = db.query(models.Schools).filter(models.Schools.name == school_name)
    school.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
        '/{school_name}/students', 
        tags=["schools", "students"],
        response_model=List[schemas.Student]
        )
def get_students_from_school(school_name: str, db: Session = Depends(get_db)):
    """
    param: school name
    returns: all student objects enrolled in given school if exists
    """
    students = db.query(models.Students).filter(models.Students.school == school_name).order_by(models.Students.name).all()
    return students


@router.get('/{school_name}/{cohort_name}/{step_nbr}/progress', tags=["schools", "cohorts", "students", "milestones"])
def get_student_progress_for_school_cohort(school_name: str, cohort_name: str, step_nbr, db: Session = Depends(get_db)):
    """Fetches the percentage of how many students from specified school and cohort has achieved a specified milestone.

    Args:
        school_name: Name of the school.
        cohort_name: Name of the cohort.
        step_nbr: An int specifying which step of the milestones.

    Returns:
        A percentage of how many students have achieved the specified milestone or more.
    """
    students_count = db.query(models.Students.milestones_achieved).filter(models.Students.school == school_name, models.Students.cohort == cohort_name).count()
    students_achieved_milestone_count = db.query(models.Students.milestones_achieved).filter(models.Students.school == school_name, models.Students.cohort == cohort_name, models.Students.milestones_achieved >= step_nbr).count()
    if students_count == 0:
        return 0
    return students_achieved_milestone_count/students_count