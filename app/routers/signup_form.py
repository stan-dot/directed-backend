from fastapi import Depends, HTTPException, Header, Request, status, Response, APIRouter
from fastapi.responses import JSONResponse
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import or_
from .. import models
from .. import schemas
import hmac
import hashlib
import base64
from typing import List, Optional

router = APIRouter(prefix="/signup_form", tags=["surveys", "signup_form"])

YOUR_SIGNING_SECRET = "test"


# POST endpoint for signup surveys
# https://tally.so/help/webhooks#cf468d8f66d74fbf9363f6d0fd975d81
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    tags=["signup_form_submission"],
    response_model=schemas.Milestone,
)
async def create_milestone(
    request: Request, tally_signature: str = Header(None), db: Session = Depends(get_db)
):
    webhook_payload = await request.json()
    calculated_signature = base64.b64encode(
        hmac.new(
            key=YOUR_SIGNING_SECRET, msg=request.body, digestmod=hashlib.sha256
        ).digest()
    ).decode()

    if tally_signature == calculated_signature
        # signature is valid, process the webhook payload
        return JSONResponse(content={"message": "Webhook received and processed successfully."}, status_code=status.HTTP_200_OK)
    else:
        # Signature is invalid, reject the webhook request
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid signature.")


    old_milestone = db.query(models.Milesones).get(
        {"cohort_name": milestone.cohort_name, "step_nbr": milestone.step_nbr}
    )
    if old_milestone:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"milestone with step number: {milestone.step_nbr} in Cohort: {milestone.cohort_name} already exist, cannot create a new one with the same name.",
        )
    new_milestone = models.Milesones(**milestone.dict())
    db.add(new_milestone)
    db.commit()
    db.refresh(new_milestone)
    return new_milestone


# CRUD for students
@router.post("/", response_model=schemas.Student)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    """
    creates a new student given a student object is it doesn't already exist
    returns the new student
    """
    
    cohort = db.query(models.Cohorts).get(student.cohort_id)
    if not cohort:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cohort not found"
        )

    new_pseudonym = generate_pseudonym(cohort.pseudonym_prefix)

    new_student_data = student.dict()
    new_student = models.Students(**new_student_data, pseudonym=new_pseudonym)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student
