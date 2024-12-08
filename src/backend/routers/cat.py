from fastapi import APIRouter, HTTPException
from sqlmodel import SQLModel, select
from models import AnswersCats, QuestionCats
from dependencies import SessionDep


router = APIRouter(
    prefix="/cat",
    tags=["cat"],
    responses={404: {"desctiption": "Not found"}},
)

class QuestionCatsBase(SQLModel):
    question: str

class QuestionCatsPublic(QuestionCatsBase):
    question: str

class AnswersCatsBase(SQLModel):
    answers: str

class AnswersCatsPublic(AnswersCatsBase):
    answers: str

class Cat_breedBase(SQLModel):
    name: str

class Cat_breedPublic(Cat_breedBase):
    name: str
    description: str
    activity: str
    wool: str
    personality: str
    communication: str
    allergy: str
    care: str
    image: str
#вопросы
@router.get("/question/{question_id}")
def read_answers_by_question_id(question_id: int, db: SessionDep):
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