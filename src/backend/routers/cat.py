from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import SQLModel, select
from models import AnswersCats, QuestionCats
from dependencies import SessionDep
from auth.oauth2 import get_current_user
from schemas import UserBase
router = APIRouter(
    prefix="/cat",
    tags=["cat"],
    responses={404: {"desctiption": "Not found"}},
)


@router.get("/question/{question_id}")
def read_answers_by_question_id(question_id: int, db: SessionDep, current_user: UserBase = Depends(get_current_user)):
    answersCats = db.exec(select(AnswersCats).where(AnswersCats.id_question == question_id)).all()
    if not answersCats:
        raise HTTPException(status_code=404, detail="Ответы не найдены для данного вопроса")
    question = db.exec(select(QuestionCats).where(QuestionCats.id_question == question_id)).first()
    
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
        for answer in answersCats
    ]
    
    return question_data, answers_data
