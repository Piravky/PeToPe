from pydantic import BaseModel

class UserBase(BaseModel):
    id: int
    name: str


class UserPublic(UserBase):
    score_cat: int
    score_dog: int

class UserCreate(UserBase):
    email: str
    password: str
    name: str
    score_cat: int | None = None
    score_dog: int | None = None


class UserUpdate(UserBase):
    name: str | None = None
    password: str | None = None
    email: str | None = None
    score_cat: int | None = None
    score_dog: int | None = None


class QuestionCatsBase(BaseModel):
    id_question: int

class QuestionCatsPublic(QuestionCatsBase):
    question: str

class AnswersCatsBase(BaseModel):
    id: int

class AnswersCatsPublic(AnswersCatsBase):
    answers: str

class Cat_breedBase(BaseModel):
    id: int

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

class QuestionDogsBase(BaseModel):
    id_question: int

class QuestionDogsPublic(QuestionCatsBase):
    question: str

class AnswersDogsBase(BaseModel):
    id: int

class AnswersDogsPublic(AnswersDogsBase):
    answers: str
    
class Dog_breedBase(BaseModel):
    id: int

class Dog_breedPublic(Dog_breedBase):
    name: str
    descrtiption: str
    activity: str
    size: str
    wool: str
    allergy: str
    communication: str
    attentiveness: int
    health_risk: str
    image: str
    
