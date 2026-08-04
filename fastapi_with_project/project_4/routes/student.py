from fastapi import APIRouter,Depends,HTTPException,Query
from sqlmodel import Session,select,func
from models import Student,StudentCreate,StudentRead,StudentUpdate
from database import get_session


router=APIRouter(
    prefix="/student", # means every endpoints starts with /student
    tags=["student"] # this groups the endpoints in the automatic swagger documentation
)


@router.post("/",response_model=StudentRead)
def create_student(student:StudentCreate,session:Session=Depends(get_session)):
    db_student=Student(**student.model_dump())
    session.add(db_student)
    session.commit()
    session.refresh(db_student)
    return db_student

@router.get("/{student_id}",response_model=StudentRead)
def get_student(student_id:int,session:Session=Depends(get_session)):
    student=session.get(Student,student_id)
    if not student:
        raise HTTPException(
            status_code=404,
            detail="No Student found with this id"
        )
    return student

@router.patch("/{student_id}",response_model=StudentRead)
def update_student(student_id:int,update:StudentUpdate,session:Session=Depends(get_session)):
    student=session.get(Student,student_id)
    if not student:
        raise HTTPException(
            status_code=404,
            detail="No Student found with this id"
        )
    update_data=update.model_dump(exclude_unset=True)
    for key,value in update_data.items():
        setattr(student,key,value)
    session.add(student)
    session.commit()
    session.refresh(student)
    return student


@router.delete("/{student_id}")
def delete_student(student_id:int,session:Session=Depends(get_session)):
    student=session.get(Student,student_id)
    if not student:
        raise HTTPException(
            status_code=404,
            detail="No student found with this id"
        )
    session.delete(student)
    session.commit()
    return {"message":"f'{student_id}' is deleted"}