from flask import Blueprint, jsonify, render_template, request, session
from database.step2_db import Step2DB
from database.step1_db import Step1DB

step2_blueprint = Blueprint('step2', __name__)

@step2_blueprint.route('/step2', methods=['GET', 'POST'])
def step2():
    user_id = session.get('selected_user_id')
    db = Step2DB('step_data.db')
    db.create_table()

    if request.method == 'POST':
        selected_summary_id = request.form['selected_summary']
        q1 = request.form['q1']
        q2 = request.form['q2']
        q3 = request.form['q3']
        
        if db.fetch_data_by_summary_id(selected_summary_id):
            db.update_data(selected_summary_id, q1, q2, q3, user_id)
        else:
            db.add_data(selected_summary_id, q1, q2, q3, user_id)

    step1_db = Step1DB('step_data.db')
    summaries = step1_db.fetch_data(user_id)  # Fetch data from step1 for the dropdown
    
    step2_entries = db.fetch_step2_with_step1(session['selected_user_id'])
    db.close()
    
    step1_db.close()
    db.close()

    return render_template('step2.html', summaries=summaries, step2_entries=step2_entries)

@step2_blueprint.route('/step2/read/<int:summary_id>', methods=['GET'])
def read_step2(summary_id):
    user_id = session.get('selected_user_id')
    if user_id:
        step2_db = Step2DB('step_data.db')
        data = step2_db.fetch_data_by_summary_id(summary_id)
        step2_db.close()

        expansion = list(data[0])
        expansion.append("<br>".join(data[0][2:5]).replace('\n', '<br>'))

        return jsonify(expansion)
    return jsonify([])

@step2_blueprint.route('/fetch_summary_details/<int:summary_id>', methods=['GET'])
def fetch_summary_details(summary_id):
    db = Step1DB('step_data.db')
    details = db.fetch_summary_details_by_id(summary_id)
    db.close()
    return jsonify(details)
