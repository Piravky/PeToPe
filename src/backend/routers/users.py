from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import select, SQLModel
from models import AnswersDogs, User, Dog_breed, AnswersCats, Cat_breed
from dependencies import SessionDep
from schemas import UserBase, UserCreate, UserPublic
from auth.oauth2 import get_current_user
from auth.utils import hash_password
from typing import Annotated

router = APIRouter(
    prefix="/users",
    tags=["user"],
    responses={404: {"desctiption": "Not found"}},
)


@router.get("/", response_model=list[UserPublic])
def read_users(
    db: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
    current_user: UserBase = Depends(get_current_user)
    ):
    users = db.exec(select(User).offset(offset).limit(limit)).all()
    return users

@router.get("/me", response_model=UserPublic)
def read_user(db: SessionDep, current_user: UserBase = Depends(get_current_user)):
    user = db.get(User, current_user.id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user

#@router.delete("/{user_id}")
#def delete_user(user_id: int, db: SessionDep):
#    user = db.get(User, user_id)
#    if not user:
#        raise HTTPException(status_code=404, detail="Пользователь не найден")
#    db.delete(user)
#    db.commit()
#    return {"ok": True}

#@router.patch("/{user_id}", response_model=UserPublic)
#def update_user(user_id: int, user: UserUpdate, db: SessionDep):
#    user_db = db.get(User, user_id)
#    if not user:
#        raise HTTPException(status_code=404, detail="Пользователь не найден")
#    user_data = user.model_dump(exclude_unset=True)
#    user_db.sqlmodel_update(user_data)
#    db.add(user_data)
#    db.commit()
#    db.refresh(user_data)
#    return user_data

@router.post("/score_none", response_model=UserPublic)
def reset_score(db: SessionDep, current_user: UserBase = Depends(get_current_user)):
    user = db.get(User, current_user.id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    user.score_cat = 0
    user.score_dog = 0
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/", response_model=UserPublic)
def create_user(user: UserCreate, db: SessionDep):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")

    hashed_password = hash_password(user.password)
    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        score_cat=0,
        score_dog=0
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/cat/sum_scores")
def sum_scores_by_question_id(answer_id: int, db: SessionDep, current_user: UserBase = Depends(get_current_user)):
    answersCats = db.exec(select(AnswersCats).where(AnswersCats.id == answer_id)).all()
    # Суммируем баллы за ответы
    total_score_cat = sum(answer.score for answer in answersCats)
   # Находим пользователя по user_id
    user = db.get(User, current_user.id)
    # Обновляем баллы пользователя
    user.score_cat += total_score_cat
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "Суммарные баллы успешно сохранены", "user_id": user.id, "total_score": user.score_cat}

@router.get("/cat_breed")
def get_cat_breed(db: SessionDep, current_user: UserBase = Depends(get_current_user)):
    # Получаем пользователя по user_id
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        return {"error": "Пользователь не найден"}
    # Считываем баллы пользователя
    user_score_cat = user.score_cat

    # Ищем породу кота с совпадающими баллами
    cat_breeds = db.query(Cat_breed).filter(
            Cat_breed.scores_min <= user_score_cat,
            Cat_breed.scores_max >= user_score_cat
            ).all()

    if cat_breeds:
        breeds_info = []
        # Если порода найдена, возвращаем информацию о ней
        for cat_breed in cat_breeds:
            breeds_info.append({
                "breed": cat_breed.name,
                "description": cat_breed.description,
                "image": cat_breed.image
                })
        return breeds_info
    else:
        return {"message": "Нет информации"}
    
@router.post("/dog/sum_scores")
def sum_scores_by_question_id(answer_id: int, db: SessionDep, current_user: UserBase = Depends(get_current_user)):
    answersDogs = db.exec(select(AnswersDogs).where(AnswersDogs.id == answer_id)).all()
    # Суммируем баллы за ответы
    total_score_dog = sum(answer.score for answer in answersDogs)
   # Находим пользователя по user_id
    user = db.get(User, current_user.id)
    # Обновляем баллы пользователя
    user.score_dog += total_score_dog
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "Суммарные баллы успешно сохранены", "user_id": user.id, "total_score": user.score_dog}


@router.get("/dog_breed")
def get_dog_breed(db: SessionDep, current_user: UserBase = Depends(get_current_user)):
    # Получаем пользователя по user_id
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        return {"error": "Пользователь не найден"}
    # Считываем баллы пользователя
    user_score_dog = user.score_dog

    # Ищем породу кота с совпадающими баллами
    dog_breeds = db.query(Dog_breed).filter(
            Dog_breed.scores_min <= user_score_dog,
            Dog_breed.scores_max >= user_score_dog
            ).all()

    if dog_breeds:
        breeds_info = []
        for dog_breed in dog_breeds:
            breeds_info.append({
                "breed": dog_breed.name,
                "description": dog_breed.description,
                "image": dog_breed.image
                })
        return breeds_info
    else:
        return {"message": "Вам стоит тщательно оценить свои возможности и готовность к уходу за питомцем, а также учитывать, что собаки могут потребовать больше времени и усилий для достижения гармонии в отношениях с хозяином и окружающими."}
