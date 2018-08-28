import psycopg2


class MyDatabase():
    """ Class for Creating  a Database and the SQL Queries"""

    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                dbname='stackoverflow', user='postgres', host='localhost',
                password='oscarkirex', port='5432')

            self.connection.autocommit = True
            self.cur = self.connection.cursor()
            self.create_tables()
        except psycopg2.Error as error:
            return error

    def create_tables(self):
        Users_table = """CREATE TABLE IF NOT EXISTS UserTable (User_ID TEXT PRIMARY KEY,
        email varchar(50) NOT NULL UNIQUE, password varchar(50) NOT NULL)"""
        self.cur.execute(Users_table)

        questions_table = """CREATE TABLE IF NOT EXISTS QuestionTable
        (Question_ID TEXT PRIMARY KEY, Title TEXT NOT NULL UNIQUE,
        body varchar(50) NOT NULL, tags varchar(50) NOT NULL,
        created_at TIMESTAMP)"""
        self.cur.execute(questions_table)

        answers_table = """CREATE TABLE IF NOT EXISTS AnswerTable
        (Answer_ID TEXT PRIMARY KEY, Answer TEXT NOT NULL UNIQUE,
        created_at TIMESTAMP) """
        self.cur.execute(answers_table)

    # def drop_tables(self):
    #     drop_Users_table = """DROP TABLE IF EXISTS UserTable CASCADE"""
    #     drop_questions_table = """DROP TABLE IF EXISTS QuestionTable CASCADE"""
    #     drop_answers_table = """DROP TABLE IF EXISTS AnswerTable CASCADE"""

    #     self.cur.execute(drop_Users_table)
    #     self.cur.execute(drop_questions_table)
    #     self.cur.execute(drop_answers_table)

    def create_user(self, sql):
        self.cur.execute(sql)
        result = self.cur.fetchone()
        return result

    def check_user_exists(self, query):
        self.cur.execute(query)
        result = self.cur.fetchone()
        return result

    def fetch_user(self, sql):
        self.cur.execute(sql)
        result = self.cur.fetchone()
        return result


    def close(self):
        self.cur.close()
        self.connection.close()


if __name__ == '__main__':
    db = MyDatabase()
    db.create_tables()
    # db.drop_tables()
