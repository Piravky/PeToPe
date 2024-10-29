from fastapi import APIRouter, Query, HTTPException
from sqlmodel import SQLModel, Field, select
from typing import Annotated
from ..dependencies import SessionDep

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

@router.get("/question/{id_question}", response_model=QuestionCatsPublic)
def read_questionCats(id_question: int, session: SessionDep):
    questionCats = session.get(QuestionCats, id_question)
    if not questionCats:
        raise HTTPException(status_code=404, detail="Вопрос не найден")
    return questionCats #TODO добавить добавление ответов к возвращаемому значению

# @router.get("/answersCats/question/{question_id}", response_model=list[AnswersCatsPublic])
# def read_answers_by_question_id(question_id: int, session: SessionDep):
#     answersCats = session.exec(select(AnswersCats).where(AnswersCats.id_question == question_id)).all()
#     if not answersCats:
#         raise HTTPException(status_code=404, detail="Ответы не найдены для данного вопроса")
#     return answersCats
