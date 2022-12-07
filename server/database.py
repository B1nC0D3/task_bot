from sqlalchemy import Column, DateTime, Integer, String, create_engine, func
from sqlalchemy.orm import Session, declarative_base

engine = create_engine('sqlite:///sqlite3.db', echo=True)
session = Session(engine)
Base = declarative_base()


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    description = Column(String)
    created = Column(DateTime, server_default=func.now())

    def __str__(self) -> str:
        return self.description


Base.metadata.create_all(engine)
