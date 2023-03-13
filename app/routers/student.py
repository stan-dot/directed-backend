from fastapi import Depends, HTTPException, status, Response, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models
from .. import schemas
from typing import List

router=APIRouter(
    prefix='/students',
    tags=["students"]
    )


#CRUD for students
@router.post(
        '/', 
        response_model=schemas.Student
        )
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    """
    creates a new student given a student object is it doesn't already exist
    returns the new student
    """
    old_student = db.query(models.Students).get(ident=student.personal_id)
    if old_student:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"student with id: {student.personal_id} already exist, cannot create a new one with the same name.")
    student.gender = student.gender.value
    new_student = models.Students(**student.dict())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


@router.get(
        '/', 
        response_model=List[schemas.Student]
        )
def get_students(db: Session = Depends(get_db)):
    """
    returns all student objects
    """
    students = db.query(models.Students).all()
    return students


@router.get(
        '/{personal_id}', 
        response_model=schemas.Student
        )
def get_student(personal_id:str, db: Session = Depends(get_db)):
    """
    returns student object by personal id in the format 19xxxxxx-xxxx or 20xxxxxx-xxxx
    """
    student = db.query(models.Students).get(personal_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"student with personal id: {personal_id} not found!"
            )
    return student


@router.put(
        '/{personal_id}', 
        response_model=schemas.Student
        )
def update_student(personal_id: str, updated_student: schemas.StudentCreate, db: Session = Depends(get_db)):
    student_query = db.query(models.Students).filter(models.Students.personal_id == personal_id)
    student = student_query.first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"student with personal id: {personal_id} not found!"
            )
    updated_student.gender = updated_student.gender.value
    student_query.update(updated_student.dict(), synchronize_session=False)
    db.commit()
    return updated_student
    

@router.delete('/{personal_id}')
def delete_student(personal_id:str, db: Session = Depends(get_db)):
    student = db.query(models.Students).filter(models.Students.name == personal_id)
    student.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Other

@router.get(
        '/{school_name}/{cohort_name}', 
        tags=["cohorts", "students", "schools"],
        response_model=List[schemas.Student]
        )
def get_students_from_cohort_school(cohort_name: str, school_name: str, db: Session = Depends(get_db)):
    """
    param: cohort name, school name
    returns: all student objects enrolled in given cohort if exists
    """
    students = db.query(models.Students).filter(
        models.Students.cohort == cohort_name, 
        models.Students.school == school_name
        ).order_by(models.Students.name).all()
    return students


@router.get('/{personal_id}/cardanowallet')
def get_students_from_cohort(personal_id: str, db: Session = Depends(get_db)):
    """
    param: student personal id
    returns: the student's carnado wallet address
    """
    student = db.query(models.Students).get(personal_id)
    if not isinstance(student, models.Students):
        raise HTTPException(
             status_code=status.HTTP_404_NOT_FOUND,
             detail=f"student with personal id {personal_id} not found!"
             )
    return student.cardano_wallet