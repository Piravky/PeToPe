from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from sqlmodel import SQLModel, Field, select

router = APIRouter(
    prefix="/cat",
    tags=["cat"],
    responses={404: {"desctiption": "Not found"}},
)

class QuestionCatsBase(SQLModel):
    question: str

class QuestionCats(SQLModel, table=True):
    __tablename__ = "QuestionCats"

    id_question: int | None = Field(default=None, primary_key=True)
    question: str

class QuestionCatsPublic(QuestionCatsBase):
    question: str

class AnswersCatsBase(SQLModel):
    answers: str        

class AnswersCats(SQLModel, table=True):
    __tablename__ = "AnswersCats"

    id: int | None = Field(default=None, primary_key=True)
    answers: str
    score: int
    id_question: int

class AnswersCatsPublic(AnswersCatsBase):
    answers: str

class Cat_breedBase(SQLModel):
    name: str

class Cat_breed(SQLModel, table=True):
    __tablename__ = "cats"

    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str
    activity: str
    size: str
    wool: str
    allergy: str
    communication: str
    allergy: str
    care: str
    scores: int

class Cat_breedPublic(Cat_breedBase):
    name: str
    description: str
    activity: str
    wool: str
    personality: str
    communication: str
    allergy: str
    care: str

@router.get("/answers/question/{question_id}")
def read_answers_by_question_id(db: Session, question_id: int):
    answersCats = db.exec(select(AnswersCats).where(AnswersCats.id_question == question_id)).all()
    if not answersCats:
        raise HTTPException(status_code=404, detail="Ответы не найдены для данного вопроса")
    question = db.exec(select(QuestionCats).where(QuestionCats.id_question == question_id)).first()
    
    if not question:
        raise HTTPException(status_code=404, detail="Вопрос не найден")
    
    question_data = question.question
    
    answers_data = [
        (
            answer.answers
        )
        for answer in answersCats
    ]
    
    return question_data, answers_data