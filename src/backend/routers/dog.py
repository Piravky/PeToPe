from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from sqlmodel import SQLModel, Field, select

router = APIRouter(
    prefix="/dog",
    tags=["dog"],
    responses={404: {"desctiption": "Not found"}},
)

class QuestionDogsBase(SQLModel):
    question: str

class QuestionDogs(SQLModel, table=True):
    __tablename__ = "QuestionDogs"

    id_question: int | None = Field(default=None, primary_key=True)
    question: str

class QuestionDogsPublic(QuestionDogsBase):
    question: str


class AnswersDogsBase(SQLModel):
    answers: str

class AnswersDogs(SQLModel, table=True):
    __tablename__ = "AnswersDogs"

    id: int | None = Field(default=None, primary_key=True)
    answers: str
    score: int
    id_question: int

class AnswersDogsPublic(AnswersDogsBase):
    answers: str


class Dog_breedBase(SQLModel):
    name: str

class Dog_breed(SQLModel, table=True):
    __tablename__ = "dogs"

    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str
    activity: str
    size: str
    wool: str
    allergy: str
    communication: str
    attentiveness: int
    health_risks: str
    scores: int

class Dog_breedPublic(Dog_breedBase):
    name: str
    description: str
    activity: str
    size: str
    wool: str
    allergy: str
    communication: str
    attentiveness: int
    health_risks: str

@router.get("/answers/question/{question_id}")
def read_answers_by_question_id(db: Session, question_id: int):
    answersDogs = db.exec(select(AnswersDogs).where(AnswersDogs.id_question == question_id)).all()
    if not answersDogs:
        raise HTTPException(status_code=404, detail="Ответы не найдены для данного вопроса")
    question = db.exec(select(QuestionDogs).where(QuestionDogs.id_question == question_id)).first()
    
    if not question:
        raise HTTPException(status_code=404, detail="Вопрос не найден")
    
    question_data = question.question
    
    answers_data = [
        (
            answer.answers
        )
        for answer in answersDogs
    ]
    
    return question_data, answers_data