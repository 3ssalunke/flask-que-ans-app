import os
from flask import Flask, render_template, request, session, redirect, url_for
from db import database
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)


def get_current_user():
    user = None
    if 'user' in session:
        user = database.get_user_by_name(session['user'])
    return user


@app.route('/')
def index():
    user = get_current_user()
    questions_with_answers = database.get_all_answered_questions()
    return render_template('home.html', user=user, qwas=questions_with_answers)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        check_user = database.get_user_by_name(name)
        if check_user:
            return render_template('register.html', error='User Already Exists!')
        hashed_pass = generate_password_hash(request.form['password'], method='sha256')
        database.insert_users(name, hashed_pass, 0, 0)
        session['user'] = name
        return redirect(url_for('index'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        user = database.get_user_by_name(name)
        if user:
            if check_password_hash(user['password'], password):
                session['user'] = user['name']
                return redirect(url_for('index'))
            else:
                message='Password was incorrect.'
        else:
            message='Username is not present. Please register.'
    return render_template('login.html', message=message)


@app.route('/question/<question_id>')
def question(question_id):
    user = get_current_user()
    question = database.get_queans_by_id(question_id)
    return render_template('question.html', user=user, question=question)


@app.route('/answer/<question_id>', methods=['GET', 'POST'])
def answer(question_id):
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    if user['expert'] == 0:
        return redirect(url_for('index'))
    if request.method == 'POST':
        database.update_question_answer(question_id, request.form['answer'])
        return redirect(url_for('unanswered'))
    question = database.get_question_by_id(question_id)
    return render_template('answer.html', user=user, question=question)


@app.route('/ask', methods=['GET', 'POST'])
def ask():
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    if request.method == 'POST':
        question = request.form['question']
        expert_id = request.form['expert']
        asked_id = user['id']
        database.insert_questions(question,asked_id,expert_id)
    all_experts = database.get_all_experts()
    return render_template('ask.html', user=user, experts=all_experts)


@app.route('/unanswered')
def unanswered():
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    if user['expert'] == 1:
        questions = database.get_unanswered_question_by_expert(user['id'])
        return render_template('unanswered.html', user=user, questions=questions)
    return redirect(url_for('index'))


@app.route('/users')
def users():
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    if user['admin'] == 1:
        users = database.get_all_db_users()
        return render_template('users.html', user=user, users=users)
    return redirect(url_for('index'))


@app.route('/promote/<user_id>')
def promote(user_id):
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    if user['admin'] == 1:
        database.update_to_expert(user_id)
        return redirect(url_for('users'))
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)