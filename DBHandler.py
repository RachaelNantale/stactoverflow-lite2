import psycopg2
import psycopg2.extras as extras


class MyDatabase():
    """ Class for Creating  a Database and the SQL Queries"""

    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                dbname='d9ia0m2p0lvc8',
                user='rtoxgqqxlywlsz',
                host='ec2-174-129-25-182.compute-1.amazonaws.com',
                password='09919598c10eb10a8246f16bc709f4dfbf12c719b2ae72b72fac95cbc214daff',
                port='5432')

            self.connection.autocommit = True
            self.cursor = self.connection.cursor()

            self.create_tables()
        except psycopg2.Error as error:
            print(error)

    def create_tables(self):
        Users_table = """CREATE TABLE IF NOT EXISTS UserTable (User_ID TEXT PRIMARY KEY,
        email varchar(50) NOT NULL UNIQUE, password varchar(50) NOT NULL)"""
        self.cursor.execute(Users_table)

        questions_table = """CREATE TABLE IF NOT EXISTS QuestionTable
        (Title TEXT NOT NULL UNIQUE,
        body varchar(50) NOT NULL, tags varchar(50) NOT NULL,
        asked_by varchar(50) NOT NULL,
        created_at TIMESTAMP,Question_ID SERIAL PRIMARY KEY, QtnID SERIAL)"""
        self.cursor.execute(questions_table)

        answers_table = """CREATE TABLE IF NOT EXISTS AnswerTable
        (created_at TIMESTAMP,
        Answer TEXT NOT NULL,
        Question_ID SERIAL, FOREIGN KEY(Question_ID)
        REFERENCES QuestionTable(Question_ID)
        ON DELETE CASCADE ON UPDATE CASCADE,
        answered_by varchar(50) NOT NULL,
        status bool DEFAULT False,
        Answer_ID SERIAL PRIMARY KEY

        ) """
        self.cursor.execute(answers_table)

    def drop_tables(self):
        drop_Users_table = """DROP TABLE IF EXISTS UserTable CASCADE"""
        drop_questions_table = """DROP TABLE IF EXISTS QuestionTable CASCADE"""
        drop_answers_table = """DROP TABLE IF EXISTS AnswerTable CASCADE"""

        self.cursor.execute(drop_Users_table)
        self.cursor.execute(drop_questions_table)
        self.cursor.execute(drop_answers_table)

    def create_item(self, sql):
        self.cursor.execute(sql)
        return {'message': 'Created succesfully'}, 201

    def check_item_exists(self, query):
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if result:
            return True
        return False

    def fetch_user(self, sql):
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        print(result)
        return result

    def fetch_all_questions(self):
        self.cursor.execute(
            "SELECT * FROM QuestionTable;")
        questions = self.cursor.fetchall()
        my_questions = []
        for question in questions:
            my_dict = {}
            my_dict['Question_ID'] = question[5]
            my_dict['title'] = question[0]
            my_dict['description'] = question[1]
            my_dict['tags'] = question[2]
            my_dict['By'] = question[3]
            my_dict['Time'] = question[4]

            my_questions.append(my_dict)
        return my_questions

    def fetch_single_question(self, Question_ID):

        self.cursor.execute(
            "SELECT * FROM QuestionTable WHERE Question_ID = '{}' ".format(Question_ID))
        question = self.cursor.fetchone()
        my_question = []
        if question:
            my_dict = {}
            my_dict['Question_ID'] = question[5]
            my_dict['title'] = question[0]
            my_dict['description'] = question[1]
            my_dict['tags'] = question[2]
            my_dict['Asked  By'] = question[3]
            my_dict['time'] = question[4]
            my_question.append(my_dict)
            return my_question
        return None

    def fetch_single_question_by_id(self, Question_ID):
        self.cursor.execute(
            "SELECT * FROM QuestionTable WHERE Question_ID = '{}' ".format(Question_ID))
        question = self.cursor.fetchone()
        if question:
            return question

    def fetch_answer_by_id(self, Answer_ID):
        self.cursor.execute(
            "SELECT * FROM AnswerTable WHERE  Answer_ID = '{}'".format(Answer_ID))
        answer = self.cursor.fetchone()
        if answer:
            return answer

    def fetch_user_by_email(self, email):
        self.cursor.execute(
            "SELECT * FROM Usertable WHERE email = '{}'".format(email))
        email = self.cursor.fetchone()
        if email:
            return email
        self.connection.commit()

    def check_answer_exists(self, Question_ID, answer):
        self.cursor.execute(
            "SELECT  * FROM ANswerTable  WHERE Question_Id = '{}' and  answer = '{}'".format(Question_ID, answer))
        answer = self.cursor.fetchone()
        if answer:
            return True
        return False

    def fetch_answer_details(self, Question_ID, Answer_ID):
        self.cursor.execute(
            "SELECT * FROM AnswerTable WHERE Question_ID = '{}' and Answer_ID = '{}'".format(Question_ID, Answer_ID))
        details = self.cursor.fetchone()
        return details

    def fetch_all_answers(self, Question_ID):
        self.cursor.execute("SELECT * FROM QuestionTable WHERE Question_ID = '{}'".format(
            Question_ID))
        question = self.cursor.fetchone()
        self.cursor.execute(
            "SELECT * FROM AnswerTable where Question_ID = '{}'".format(Question_ID))
        answers = self.cursor.fetchall()
        answers = [row for row in answers]
        my_answers = []
        for index in range(len(answers)):
            user_answers = (
                {
                    'Answer_ID': answers[index][5],
                    'created at': answers[index][0],
                    'answer': answers[index][1],
                    'Answered by': answers[index][3],
                    'Status': answers[index][4]

                })
            my_answers.append(user_answers)
        return [{'title': question[1],
                 'Description': question[2],
                 'tags': question[3],
                 'answers': my_answers,
                 'Asked by': question[4]

                 }]

    def update_answer(self, answer, Answer_ID, Question_ID):
        try:
            self.cursor.execute("UPDATE AnswerTable SET answer = '{}' WHERE Answer_ID = '{}' and Question_ID = '{}'" .format(
                answer, Answer_ID, Question_ID))
            cmd = self.cursor.rowcount
            self.connection.commit()
            if (cmd) > 0:
                return "Update succesful"
            else:
                return "Answer not updated, or doesn't exist"

        except Exception as exception:
            return {"message": str(exception)}, 400

    def accept_answer(self,  Answer_ID):

        # try:
        query = "UPDATE AnswerTable SET status = TRUE WHERE Answer_ID = '{}';" .format(
            Answer_ID)
        ans = self.cursor.execute(query, [Answer_ID])
        return ans

    def delete_record(self, Question_ID):
        try:

            query = "DELETE FROM QuestionTable WHERE Question_ID='{}'".format(
                Question_ID)
            self.cursor.execute(query)
            delete_cmd = self.cursor.rowcount
            if delete_cmd > 0:
                return {'message': 'succesfully deleted'}, 200
            return {'message': 'Question Id doesnt exist'}, 400
        except Exception as exp:
            return {"message": str(exp)}, 400

    def close(self):
        self.cursor.close()
        self.connection.close()


if __name__ == '__main__':
    db = MyDatabase()
    db.create_tables()
