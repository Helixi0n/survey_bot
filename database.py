from sqlalchemy import create_engine, Column, Integer, Text, String, JSON, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///school.db')

Session = sessionmaker(bind=engine)
session = Session()

BaseModel = declarative_base()

class User(BaseModel):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String)

    survey = relationship('Survey', back_populates='user_id')

class Survey(BaseModel):
    __tablename__ = 'survey'

    id = Column(Integer, primary_key=True)
    passed = Column(Integer)
    title = Column(String)
    description = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))
    
    user = relationship('User', back_populates='survey')
    questions = relationship('Question', back_populates='survey')

class Question(BaseModel):
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True)
    survey_id = Column(Integer, ForeignKey('survey.id'))
    question_title = Column(Text)
    answers_data = Column(JSON, default={})

    survey = relationship('Survey', back_populates='questions')

def init_db():
    engine = create_engine("sqlite:///data.db")
    BaseModel.metadata.create_all(engine)

def get_connection():
    engine = create_engine('sqlite:///data.db')
    return sessionmaker(bind=engine)