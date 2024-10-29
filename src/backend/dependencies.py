from sqlalchemy import create_engine
#подключение к бд
from sqlalchemy.ext.declarative import declarative_base
#базовый класс
from sqlalchemy.orm import sessionmaker
#создание объектов

SQLALCHEMY_DATABASE_URL = "sqlite:///backend/sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
#создание движка бд
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)
#создаем класс сессии
#utocommit=False и autoflush=False указывают, что изменения не будут автоматически сохраняться и сбрасываться
Base = declarative_base()
#базовый класс