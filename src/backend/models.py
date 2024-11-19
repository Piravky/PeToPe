from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    score_cat: int | None = None
    score_dog: int | None = None
    email: str
    password: str
    name: str


class AnswersDogs(SQLModel, table=True):
    __tablename__ = "AnswersDogs"

    id: int | None = Field(default=None, primary_key=True)
    answers: str
    score: int
    id_question: int


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


class QuestionDogs(SQLModel, table=True):
    __tablename__ = "QuestionDogs"

    id_question: int | None = Field(default=None, primary_key=True)
    question: str


class AnswersCats(SQLModel, table=True):
    __tablename__ = "AnswersCats"

    id: int | None = Field(default=None, primary_key=True)
    answers: str
    score: int
    id_question: int


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
    care: str
    scores_max: int
    scores_min: int


class QuestionCats(SQLModel, table=True):
    __tablename__ = "QuestionCats"

    id_question: int | None = Field(default=None, primary_key=True)
    question: str
