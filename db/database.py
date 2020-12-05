from .database_connection_cm import DatabaseConnection


def create_users_table():
    with DatabaseConnection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            'CREATE TABLE IF NOT EXISTS users(id integer primary key autoincrement, name text not null, password text not null, expert boolean not null, admin boolean not null)'
        )


def create_questions_table():
    with DatabaseConnection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            'CREATE TABLE IF NOT EXISTS questions(id integer primary key autoincrement, question text not null, ans_text text, asked_id integer not null, expert_id integer not null)'
        )


def insert_users(name, password, expert, admin):
    with DatabaseConnection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            'INSERT INTO users(name, password, expert, admin) VALUES (?, ?, ?, ?)',
            [name, password, expert, admin]
        )


def insert_questions(question, asked_id, expert_id):
    with DatabaseConnection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            'INSERT INTO questions(question, asked_id, expert_id) VALUES (?, ?, ?)',
            [question, asked_id, expert_id]
        )


def get_all_db_users():
    with DatabaseConnection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            'SELECT * FROM users'
        )
        users = [{'id': user[0], 'name': user[1], 'password': user[2], 'expert': user[3], 'admin': user[4],} for user in cursor.fetchall()]
        return users


def get_user_by_name(name):
    with DatabaseConnection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            'SELECT * FROM users WHERE name = ?', [name]
        )
        res = cursor.fetchone()
        if res:
            user = {'id':res[0], 'name': res[1], 'password': res[2], 'expert': res[3], 'admin': res[4],}
            return user
        return None


def get_all_experts():
    with DatabaseConnection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            'SELECT * FROM users WHERE expert=1'
        )
        all_experts = [{'id': user[0], 'name': user[1]} for user in cursor.fetchall()]
        return all_experts


def get_unanswered_question_by_expert(expert_id):
    with DatabaseConnection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            'SELECT questions.id, questions.question, users.name FROM questions JOIN users on users.id = questions.asked_id WHERE questions.ans_text is null and questions.expert_id=?', [expert_id]
        )
        questions = [{'id': question[0], 'question': question[1], 'asked_name': question[2]} for question in cursor.fetchall()]
        return questions    


def get_question_by_id(question_id):
    with DatabaseConnection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            'SELECT id, question FROM questions WHERE id=?', [question_id]
        )
        question = cursor.fetchone()
        if question:
            return {'id': question[0], 'question': question[1]}
        return None


def get_all_answered_questions():
    with DatabaseConnection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            'SELECT questions.id, questions.question, askers.name, experts.name FROM questions JOIN users AS askers ON askers.id=questions.asked_id JOIN users AS experts ON experts.id=questions.expert_id WHERE questions.ans_text is not null'
        )

        return [ {'id': question[0], 'question': question[1], 'asked_by': question[2], 'answered_by': question[3]} for question in cursor.fetchall()]


def get_queans_by_id(question_id):
    with DatabaseConnection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            'SELECT questions.id, questions.question, questions.ans_text, askers.name, experts.name FROM questions JOIN users AS askers ON askers.id=questions.asked_id JOIN users AS experts ON experts.id=questions.expert_id WHERE questions.id=?', [question_id]
        )
        queans = cursor.fetchone()
        if queans:
            return queans
        return None

def update_to_expert(user_id):
    with DatabaseConnection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            'UPDATE users SET expert=1 WHERE id = ?', [user_id]
        )


def update_question_answer(question_id, answer):
    with DatabaseConnection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            'UPDATE questions SET ans_text=? WHERE id=?', [answer,question_id]
        )
