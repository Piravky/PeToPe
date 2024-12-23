from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import SQLModel, select
from models import AnswersDogs, QuestionDogs
from dependencies import SessionDep
from schemas import UserBase
from auth.oauth2 import get_current_user

router = APIRouter(
    prefix="/dog",
    tags=["dog"],
    responses={404: {"desctiption": "Not found"}},
)


@router.get("/question/{question_id}")
def read_answers_by_question_id(question_id: int, db: SessionDep, current_user: UserBase = Depends(get_current_user)):
    answersDogs = db.exec(select(AnswersDogs).where(AnswersDogs.id_question == question_id)).all()
    if not answersDogs:
        raise HTTPException(status_code=404, detail="Ответы не найдены для данного вопроса")
    question = db.exec(select(QuestionDogs).where(QuestionDogs.id_question == question_id)).first()

    if not question:
        raise HTTPException(status_code=404, detail="Вопрос не найден")

    question_data = {
            "id": question.id_question,
            "question": question.question
        }

    answers_data = [
        {
            "id": answer.id, 
            "answer": answer.answers
        }
        for answer in answersDogs
    ]

    return question_data, answers_data
