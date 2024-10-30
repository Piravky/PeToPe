from fastapi import APIRouter, HTTPException
from sqlmodel import select, SQLModel
from models import AnswersDogs, User, Dog_breed, AnswersCats, Cat_breed
from dependencies import SessionDep

router = APIRouter(
    prefix="/users",
    tags=["user"],
    responses={404: {"desctiption": "Not found"}},
)

class UserBase(SQLModel):
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


# @router.get("/", response_model=list[UserPublic])
# def read_users(
#     offset: int = 0,
#     db: SessionDep,
#     limit: Annotated[int, Query(le=100)] = 100
#     ):
#     users = db.exec(select(User).offset(offset).limit(limit)).all()
#     return users

@router.get("/{user_id}", response_model=UserPublic)
def read_user(user_id: int, db: SessionDep):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: SessionDep):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    db.delete(user)
    db.commit()
    return {"ok": True}

@router.patch("/{user_id}", response_model=UserPublic)
def update_user(user_id: int, user: UserUpdate, db: SessionDep):
    user_db = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    user_data = user.model_dump(exclude_unset=True)
    user_db.sqlmodel_update(user_data)
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return user_data

@router.post("/", response_model=UserPublic)
def create_user(user: UserCreate, db: SessionDep):
    db_user = User.model_validate(user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/cat/sum_scores/{user_id}")
def sum_scores_by_question_id(answer_id: int, user_id: int, db: SessionDep):
    answersCats = db.exec(select(AnswersCats).where(AnswersCats.id == answer_id)).all()
    # Суммируем баллы за ответы
    total_score_cat = sum(answer.score for answer in answersCats)
   # Находим пользователя по user_id
    user = db.get(User, user_id)
    # Обновляем баллы пользователя
    user.score_cat += total_score_cat
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "Суммарные баллы успешно сохранены", "user_id": user.id, "total_score": user.score_cat}

@router.get("/users/{user_id}/cat_breed")
def get_cat_breed(user_id: int, db: SessionDep):
    # Получаем пользователя по user_id
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"error": "Пользователь не найден"}
    # Считываем баллы пользователя
    user_score_cat = user.score_cat

    # Ищем породу кота с совпадающими баллами
    cat_breed = db.query(Cat_breed).filter(Cat_breed.scores == user_score_cat).first()

    if cat_breed:
        # Если порода найдена, возвращаем информацию о ней
        return {
            "Порода": cat_breed.name,
            "Описание": cat_breed.description,
            "points_required": cat_breed.scores
        }
    else:
        return {"message": "Нет информации"}
    
@router.post("dog/sum_scores/{answer_id}/{user_id}")
def sum_scores_by_question_id(answer_id: int, user_id: int, db: SessionDep):
    answersDogs = db.exec(select(AnswersDogs).where(AnswersDogs.id == answer_id)).all()
    # Суммируем баллы за ответы
    total_score_dog = sum(answer.score for answer in answersDogs)
   # Находим пользователя по user_id
    user = db.get(User, user_id)
    # Обновляем баллы пользователя
    user.score_dog += total_score_dog
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "Суммарные баллы успешно сохранены", "user_id": user.id, "total_score": user.score_dog}


@router.get("/users/{user_id}/dog_breed")
def get_dog_breed(user_id: int, db: SessionDep):
    # Получаем пользователя по user_id
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"error": "Пользователь не найден"}
    # Считываем баллы пользователя
    user_score_dog = user.score_dog

    # Ищем породу кота с совпадающими баллами
    dog_breed = db.query(Dog_breed).filter(Dog_breed.scores == user_score_dog).first()

    if dog_breed:
        # Если порода найдена, возвращаем информацию о ней
        return {
            "Порода": dog_breed.name,
            "Описание": dog_breed.description,
            "points_required": dog_breed.scores
        }
    else:
        return {"message": "Нет информации"}