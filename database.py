import sqlite3


def init_db():
    connection = sqlite3.connect("data.db")
    cursor = connection.execute(
        """
	CREATE TABLE IF NOT EXISTS survey (
		id INTEGER PRIMARY KEY,
        user_id INTEGER,
		title TEXT NOT NULL,
		description TEXT,
        );

    CREATE TABLE IF NOT EXISTS questions (
        quesion_id INTEGER PRYMARY KEY,
        survey_id INTEGER,
        question_text TEXT NOT NULL,
        yes INTEGER,
        no INTEGER,
        answer INTEGER
        );
	"""
    )

    connection.commit()
    connection.close()


def get_connection():
    return sqlite3.connect("data.db")