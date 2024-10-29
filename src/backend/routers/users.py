from fastapi import APIRouter, HTTPException, Query
from typing import Annotated
from sqlmodel import SQLModel, Field, select
from .cat import AnswersCats, Cat_breed
from .dog import AnswersDogs, Dog_breed
from ..dependencies import SessionLocal, engine 

class UserBase(SQLModel):
    name: str 

class User(SQLModel, table=True): 
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    score_cat: int | None = None
    score_dog: int | None = None
    email: str
    password: str
    name: str

#модель для представления пользователя без конфиденциальной информации
class UserPublic(UserBase):
    id: int

# модель для создания нового пользователя
class UserCreate(UserBase):
    email: str
    password: str
    name: str
    score_cat: int | None = None
    score_dog: int | None = None

#модель для обновления информации о пользователе
class UserUpdate(UserBase):
    name: str | None = None
    password: str | None = None
    email: str | None = None
    score_cat: int | None = None
    score_dog: int | None = None

router = APIRouter(
    prefix="/users",
    tags=["user"],
    responses={404: {"desctiption": "Not found"}},
)

@router.get("/", response_model=list[UserPublic])
def read_users(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100
    ):
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users

@router.get("/{user_id}", response_model=UserPublic)
def read_user(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user

@router.delete("/{user_id}")
def delete_user(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    session.delete(user)
    session.commit()
    return {"ok": True}

@router.patch("/{user_id}", response_model=UserPublic)
def update_user(user_id: int, user: UserUpdate, session: SessionDep):
    user_db = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    user_data = user.model_dump(exclude_unset=True)
    user_db.sqlmodel_update(user_data)
    session.add(user_data)
    session.commit()
    session.refresh(user_data)
    return user_data

@router.post("/", response_model=UserPublic)
def create_user(user: UserCreate, session: SessionDep):
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.post("/sum_scores/{user_id}", tags=["user"])
def sum_scores_by_question_id(answer_id: int, user_id: int, session: SessionDep):
    answersCats = session.exec(select(AnswersCats).where(AnswersCats.id == answer_id)).all()
    # Суммируем баллы за ответы
    total_score_cat = sum(answer.score for answer in answersCats)
   # Находим пользователя по user_id
    user = session.get(User, user_id)
    # Обновляем баллы пользователя
    user.score_cat += total_score_cat
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"message": "Суммарные баллы успешно сохранены", "user_id": user.id, "total_score": user.score_cat}

@router.get("/users/{user_id}/cat_breed")
def get_cat_breed(user_id: int, session: SessionDep):
    # Получаем пользователя по user_id
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        return {"error": "Пользователь не найден"}
    # Считываем баллы пользователя
    user_score_cat = user.score_cat

    # Ищем породу кота с совпадающими баллами
    cat_breed = session.query(Cat_breed).filter(Cat_breed.scores == user_score_cat).first()

    if cat_breed:
        # Если порода найдена, возвращаем информацию о ней
        return {
            "Порода": cat_breed.name,
            "Описание": cat_breed.description,
            "points_required": cat_breed.scores
        }
    else:
        return {"message": "Нет информации"}
    
@router.post("/answersDogs/sum_scores/{answer_id}/{user_id}")
def sum_scores_by_question_id(answer_id: int, user_id: int, session: SessionDep):
    answersDogs = session.exec(select(AnswersDogs).where(AnswersDogs.id == answer_id)).all()
    # Суммируем баллы за ответы
    total_score_dog = sum(answer.score for answer in answersDogs)
   # Находим пользователя по user_id
    user = session.get(User, user_id)
    # Обновляем баллы пользователя
    user.score_dog += total_score_dog
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"message": "Суммарные баллы успешно сохранены", "user_id": user.id, "total_score": user.score_dog}


@router.get("/users/{user_id}/dog_breed")
def get_dog_breed(user_id: int, session: SessionDep):
    # Получаем пользователя по user_id
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        return {"error": "Пользователь не найден"}
    # Считываем баллы пользователя
    user_score_dog = user.score_dog

    # Ищем породу кота с совпадающими баллами
    dog_breed = session.query(Dog_breed).filter(Dog_breed.scores == user_score_dog).first()

    if dog_breed:
        # Если порода найдена, возвращаем информацию о ней
        return {
            "Порода": dog_breed.name,
            "Описание": dog_breed.description,
            "points_required": dog_breed.scores
        }
    else:
        return {"message": "Нет информации"}