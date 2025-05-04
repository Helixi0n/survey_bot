from database import get_connection, Survey, Question

session = get_connection()

class Model:
    @staticmethod
    def my_survey(survey_id):
        survey = session.query(Survey).filter(Survey.id == survey_id).first()

        return survey

    @staticmethod
    def add_survey(user_id, title, description):
        survey = Survey(title=title, description=description, user_id=user_id, passed=0)
        session.add(survey)
        session.commit()
        session.close()

    @staticmethod
    def update_survey(survey_id, question_title, *answer):
        answers = {}
        for ans in answer:
            answers[ans] = 0

        question = Question(survey_id=survey_id, question_title=question_title, answers=answers)
        session.add(question)
        session.commit()
        session.close()

    @staticmethod
    def delete_survey(survey_id):
        for_del = session.query(Survey).filter(Survey.id == survey_id).one()
        session.delete(for_del)

        for_del = session.query(Question).filter(Question.survey_id == survey_id).all()
        session.delete(for_del)

        session.commit()

    @staticmethod
    def get_my_survey_list(user_id):
        my_survey = session.query(Survey).filter(Survey.user_id == user_id).all()
        survey_list = []

        for survey in my_survey:
            survey_list.append([survey.title, survey.id])

        return survey_list
    
    @staticmethod
    def get_results(survey_id):
        pass
    
    @staticmethod
    def get_not_completed_survey_list(user_id):
        survey = session.query(Survey).filter(Survey.user_id != user_id).all()
        survey_list = []

        for surv in survey:
            survey_list.append(surv)

        return survey_list

    @staticmethod
    def complete_survey(user_id, survey_id):
        pass