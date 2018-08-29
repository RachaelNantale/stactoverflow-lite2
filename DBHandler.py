import psycopg2
import psycopg2.extras as extras


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
            print(error)

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
        (Answer_ID TEXT PRIMARY KEY,
        created_at TIMESTAMP,
        Answer TEXT NOT NULL UNIQUE,
        Question_ID TEXT, FOREIGN KEY(Question_ID)
        REFERENCES QuestionTable(Question_ID)
        ON DELETE CASCADE ON UPDATE CASCADE,
        status bool DEFAULT False
        
        ) """
        self.cur.execute(answers_table)

    def drop_tables(self):
        drop_Users_table = """DROP TABLE IF EXISTS UserTable CASCADE"""
        drop_questions_table = """DROP TABLE IF EXISTS QuestionTable CASCADE"""
        drop_answers_table = """DROP TABLE IF EXISTS AnswerTable CASCADE"""

        self.cur.execute(drop_Users_table)
        self.cur.execute(drop_questions_table)
        self.cur.execute(drop_answers_table)
# 333333

#######################################################################################################
    def create_item(self, sql):
        result = self.cur.execute(sql)
        return {'message': 'Created succesfully'}, 201

    def check_item_exists(self, query):
        self.cur.execute(query)
        result = self.cur.fetchone()
        if result:
            return True
        return False

    def fetch_user(self, sql):
        self.cur.execute(sql)
        result = self.cur.fetchone()
        return result

    def fetch_all_questions(self):
        self.cur.execute(
            "SELECT * FROM QuestionTable;")
        questions = self.cur.fetchall()
        my_questions = []
        for question in questions:
            my_dict = {}
            my_dict['Question_ID'] = question[0]
            my_dict['title'] = question[1]
            my_dict['description'] = question[2]
            my_dict['tags'] = question[3]
            my_dict['time'] = question[4]

            my_questions.append(my_dict)
        return my_questions

    def fetch_single_question(self, Question_ID):

        self.cur.execute(
            "SELECT * FROM QuestionTable WHERE Question_ID = '{}' ".format(Question_ID))
        question = self.cur.fetchall()
        my_dict = {}
        for question in question:
            if question:
                my_dict['Question_ID'] = question[0]
                my_dict['title'] = question[1]
                my_dict['description'] = question[2]
                my_dict['tags'] = question[3]
                my_dict['time'] = question[4]
                print(my_dict)
                return my_dict
            return None

    def fetch_all_answers(self, Question_ID):
        self.cur.execute("SELECT title,body,tags FROM QuestionTable WHERE Question_ID = '{}'".format(
            Question_ID))
        question = self.cur.fetchone()
        self.cur.execute(
            "SELECT * FROM AnswerTable where Question_ID = '{}'".format(Question_ID))
        answers = self.cur.fetchall()
        answers = [row for row in answers]
        my_answers = []
        for index in range(len(answers)):
            user_answers = (
                {
                    'Answer_ID': answers[index][0],
                    'created at': answers[index][1],
                    'answer': answers[index][2],
                    'status': answers[index][4]

                })
            my_answers.append(user_answers)
        return {'Question': {'title': question[0],
                             'Description': question[1],
                             'tags': question[2],
                             'answers': my_answers

                             }}

    def update_answer(self, query3):
        if self.cur.execute(query3) is None:
            return True
        return False

    def delete_record(self, Question_ID):
        try:

            query = "DELETE FROM QuestionTable WHERE Question_ID='{}'".format(
                Question_ID)
            self.cur.execute(query)
            delete_cmd = self.cur.rowcount
            if delete_cmd > 0:
                return {'message': 'succesfully deleted'}, 200
            return {'message': 'Question Id doesnt exist'}, 400
        except Exception as exp:
            return {"message": str(exp)}, 400

    def close(self):
        self.cur.close()
        self.connection.close()


if __name__ == '__main__':
    db = MyDatabase()
    db.create_tables()
    # db.drop_tables()
