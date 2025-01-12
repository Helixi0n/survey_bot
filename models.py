from survey_bot.database import get_connection

class Model:
    @staticmethod
    def add_survey(user_id, title, description):
        connection = get_connection()
        cursor = connection.execute(
            f'''
            INSERT INTO survey (user_id, title, desription)
            VALUES ({user_id}, '{title}', '{description}')
            '''
        )
        connection.commit()
        connection.close()

    @staticmethod
    def update_survey(survey_id, question):
        connection = get_connection()
        cursor = connection.execute(
            f'''
            INSERT INTO questions (survey_id, question)
            VALUES ({survey_id}, '{question}')
            '''
        )
        connection.commit()
        connection.close()

    @staticmethod
    def delete_survey(survey_id):
        connection = get_connection()
        cursor = connection.execute(
            f'''
            DELETE FROM questions
            WHERE survey_id = {survey_id}

            DELETE FROM survey 
            WHERE id = {survey_id};
            '''
        )
        connection.commit()
        connection.close()

    @staticmethod
    def get_my_survey(user_id):
        connection = get_connection()
        cursor = connection.execute(
            f'''
            SELECT title, id
            FROM survey
            WHERE user_id = {user_id}
            '''
        )
        survey = cursor.fetchall()
        connection.close()
        return survey

    @staticmethod
    def complete_survey(user_id, survey_id):
        pass