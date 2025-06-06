from sqlalchemy import create_engine, Column, Integer, Text, String, JSON, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///data.db')

Session = sessionmaker(bind=engine)
session = Session()

BaseModel = declarative_base()

user_survey_association = Table(
    'user_survey_association',
    BaseModel.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('survey_id', Integer, ForeignKey('survey.id'), primary_key=True)
)

class User(BaseModel):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String)

    complete_surveys = relationship('Survey', secondary=user_survey_association, back_populates='complete_users')
    survey = relationship('Survey', back_populates='user')

class Survey(BaseModel):
    __tablename__ = 'survey'

    id = Column(Integer, primary_key=True)
    passed = Column(Integer)
    title = Column(String)
    description = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))

    complete_users = relationship('User', secondary=user_survey_association, back_populates='complete_surveys')
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
    engine = create_engine("sqlite:///data.db")
    BaseModel.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()