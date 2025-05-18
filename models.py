from database import get_connection, Survey, Question, User

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
        for ans in answer.split('\n'):
            answers_data[ans] = 0

        question = Question(survey_id=survey_id, question_title=question_title, answers_data=answers_data)
        session.add(question)
        session.commit()
        session.close()


    @staticmethod
    def delete_survey(survey_id):
        session.query(Survey).filter(Survey.id == survey_id).delete()

        session.query(Question).filter(Question.survey_id == survey_id).delete()

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
            result[question.id] = question.answers_data

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
        survey_list = []

        for surv in survey:
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
    def write_answers(survey_id, *user_answers):
        questions = session.query(Question).filter(Question.survey_id == survey_id).all()

        