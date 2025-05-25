from database import get_connection, Survey, Question, User, user_survey_association
from sqlalchemy import select, delete, update

session = get_connection()

class Model:
    @staticmethod
    def my_survey(survey_id):
        survey = session.query(Survey).filter(Survey.id == survey_id).first()

        return survey

    @staticmethod
    def user_info_by_survey_id(survey_id):
        survey = session.query(Survey).filter(Survey.id == survey_id).first()
        user = session.query(User).filter(User.id == survey.user_id).first()

        return user
    
    @staticmethod
    def is_user_in_base(id, username):
        if not session.query(User).filter(User.id == id).first():
            session.add(User(id=id, username=username))
            session.commit()
            session.close()
        

    @staticmethod
    def add_survey(title, description, user_id):
        survey = Survey(title=title, description=description, user_id=user_id, passed=0)
        session.add(survey)
        session.commit()
        session.close()


    @staticmethod
    def update_survey(survey_id, question_title, answer):
        answers_data = {}

        quest = session.query(Question).filter(Question.survey_id == survey_id).all()
        for answer in quest:
            for key, value in answer.answers_data.items():
                answers_data[key] = 0
        
        for ans in answer.split('\n'):
            answers_data[ans] = 0

        question = Question(survey_id=survey_id, question_title=question_title, answers_data=answers_data)
        session.add(question)

        stmt = delete(user_survey_association).where(
        user_survey_association.c.survey_id == survey_id)

        session.execute(stmt)
        session.commit()
        session.close()


    @staticmethod
    def delete_survey(survey_id):
        session.query(Survey).filter(Survey.id == survey_id).delete()
        session.query(Question).filter(Question.survey_id == survey_id).delete()
        stmt = delete(user_survey_association).where(
        user_survey_association.c.survey_id == survey_id)

        session.execute(stmt)
        session.commit()
        session.close()


    @staticmethod
    def get_my_survey_list(user_id):
        my_survey = session.query(Survey).filter(Survey.user_id == user_id).all()
        survey_list = []

        for survey in my_survey:
            survey_list.append([survey.title, survey.id])

        return survey_list
    

    @staticmethod
    def get_results(survey_id):
        questions = session.query(Question).filter(Question.survey_id == survey_id).all()
        result = {}

        for question in questions:
            result[question.question_title] = question.answers_data

        return result


    @staticmethod
    def is_this_my_survey(user_id, survey_id):
        survey = session.query(Survey).filter(Survey.id == survey_id).first()
        if survey.user_id == user_id:
            return True
        return False
    

    @staticmethod
    def find_not_completed_survey_list(user_id):
        survey = session.query(Survey).filter(Survey.user_id != user_id).all()

        query = select(user_survey_association.c.survey_id).where(
        user_survey_association.c.user_id == user_id)

        result = session.execute(query)
        completed = [row[0] for row in result]
        survey_list = []

        for surv in survey:
            if surv.id not in completed:
                survey_list.append([surv.title, surv.id])

        return survey_list


    @staticmethod
    def get_questions(survey_id):
        questions = session.query(Question).filter(Question.survey_id == survey_id).all()
        question = {}

        for quest in questions:
            question[quest.question_title] = quest.answers_data

        return question
    
    @staticmethod
    def write_answers(survey_id, user_answers, user_id):
        survey = session.query(Survey).filter(Survey.id == survey_id).first()
        survey.passed += 1

        questions = session.query(Question).filter(Question.survey_id == survey_id).all()
        data = user_answers.items()
        
        for question in questions:
            for key, value in data:
                answers_data = question.answers_data
                if key == question.question_title:
                    answers_data[value] += 1

            stmt = update(Question).where(Question.id == question.id).values(answers_data=answers_data)
            session.execute(stmt)
                
        association = user_survey_association.insert().values(user_id=user_id, survey_id=survey_id)
        session.execute(association)
        
        session.commit()
        session.close()
