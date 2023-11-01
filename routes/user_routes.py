from flask import Blueprint, render_template, request, session
from database.user_db import UserDB

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        if 'name' in request.form and 'age' in request.form:
            name = request.form['name']
            age = request.form['age']
            user_db = UserDB('step_data.db')
            user_db.create_table()
            user_db.add_data(name, age)
            user_db.close()

    user_db = UserDB('step_data.db')
    user_db.create_table()
    users = user_db.fetch_data()
    user_db.close()

    if request.method == 'POST' and 'user' in request.form:
        user_id = int(request.form['user'])
        session['selected_user_id'] = user_id
        for user in users:
            if user[0] == user_id:
                session['selected_user_name'] = user[1]
                break

    return render_template('users.html', users=users)
