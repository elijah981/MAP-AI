from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for
from database.step1_db import Step1DB

step1_blueprint = Blueprint('step1', __name__)

@step1_blueprint.route('/step1', methods=['GET', 'POST'])
def step1():
    db = Step1DB('step_data.db')
    db.create_table()

    if request.method == 'POST':
        life_stage = request.form[f'life_stage']
        achievement = request.form[f'achievement']
        db.add_data(life_stage, achievement, session['selected_user_id'])

    existing_entries = db.fetch_data(session['selected_user_id'])
    db.close()

    return render_template('step1.html', existing_entries=existing_entries)

@step1_blueprint.route('/step1/delete/<int:entry_id>', methods=['POST'])
def delete_entry(entry_id):
    user_id = session.get('selected_user_id')
    if user_id:
        step1_db = Step1DB('step_data.db')
        step1_db.delete_data(entry_id, user_id)
        step1_db.close()
    return redirect(url_for('steps.step1'))
