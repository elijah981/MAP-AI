import json

from flask import (
    Blueprint,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from database.chatgpt_db import ChatGPTDB
from database.step2_db import Step2DB
from database.step4_db import Step4DB
from database.steps_summary_db import StepsSummary
from models.step4_analysis import Step4Analysis

step4_blueprint = Blueprint("step4", __name__)


@step4_blueprint.route("/step4", methods=["GET", "POST"])
def step4():
    user_id = session.get("selected_user_id")
    db = Step2DB("step_data.db")
    step2_entries = db.fetch_step2_with_step1(user_id)
    db.close()

    analysis = Step4Analysis()

    if request.method == "POST":
        if "ai_assist" in request.form:
            # Call the step4Analysis function here
            # Code for step4Analysis goes here
            pass
        elif "motivated_abilities" in request.form:
            # Store the results of the checkboxes in a step4 database
            # Code for storing checkbox results goes here
            pass
    return render_template(
        "step4.html",
        step2_entries=step2_entries,
        sub_categories=analysis.sub_categories,
        title="Motivated Abilities",
    )


@step4_blueprint.route("/step4/analyze_selected_achievement", methods=["POST"])
def analyze_selected_achievement():
    data = request.get_json()
    summary_id = data["achievementId"]
    expansion = data["achievementDetails"]
    reanalyze = data["reanalyze"]

    # Check if the response exists in the chatgpt table
    chatgpt_db = ChatGPTDB("step_data.db")
    chatgpt_db.create_table()
    entry = chatgpt_db.read_entry(summary_id, 4)
    chatgpt_db.close()

    analyzer = Step4Analysis()

    if entry and "reanalyze" not in reanalyze:
        response = json.loads(entry[4])
    else:
        # Delete the old entry from the chatgpt table if reanalyze button is pressed
        if entry:
            chatgpt_db = ChatGPTDB("step_data.db")
            chatgpt_db.create_table()
            chatgpt_db.delete_entry(summary_id, 4)
            chatgpt_db.close()

        # Get the response using the get_response function
        prompt = analyzer.generate_prompt(expansion)
        response = analyzer.get_response(prompt)
        usage = list(analyzer.usage.to_dict().values())
        usage = ";".join([str(x) for x in usage])

        # Store the response in the chatgpt table
        chatgpt_db = ChatGPTDB("step_data.db")
        chatgpt_db.create_table()
        chatgpt_db.add_entry(summary_id, 4, prompt, json.dumps(response), usage)
        chatgpt_db.close()

    tagged_text = analyzer.tag_text(expansion, "highlight", response)

    return jsonify({"tagged_text": tagged_text, "categories": response})


@step4_blueprint.route("/step4/add", methods=["POST"])
def add_step4_data():
    user_id = session.get("selected_user_id")
    step1_summary_id = request.form.get("selected_achievement")
    db = Step4DB("step_data.db")

    def generate_checkbox_name(column):
        checkbox_name = f"category_{column.replace('0_', '0_subcategory_', 1)}_checkbox"
        return checkbox_name

    # Get the boolean values from the form
    boolean_values = {}
    for column in db.boolean_columns:
        checkbox_name = generate_checkbox_name(column)
        boolean_values[column] = bool(request.form.get(checkbox_name))

    # Check if the entry exists for step1_summary_id
    if db.entry_exists(step1_summary_id):
        # Update the existing entry
        db.update(step1_summary_id, user_id, **boolean_values)
    else:
        # Add a new entry
        db.add(step1_summary_id, user_id, **boolean_values)

    db.close()

    return redirect(url_for("step4.step4"))


@step4_blueprint.route("/step4/summary/count/<user_id>")
def get_summary_count(user_id):
    db = Step4DB("step_data.db")
    count = db.get_summary_count(user_id)
    db.close()
    return jsonify({"count": count})


@step4_blueprint.route("/step4/summary", methods=["POST", "GET"])
def step4_summary():
    selected_user_id = session.get("selected_user_id")
    db = Step4DB("step_data.db")
    data = db.read_user_entries(selected_user_id)
    db.close()

    analysis = Step4Analysis()
    sub_categories = analysis.sub_categories

    totals = [sum([val[i] for val in data]) for i in range(len(data[0]))]

    if request.method == "POST":
        # Get the selected checkboxes from the form
        selected_checkboxes = list(request.form.keys())

        motivated_abilities = {}
        for cat, sub_cats in sub_categories.items():
            selections = []
            for sub in selected_checkboxes:
                if cat.lower() in sub:
                    for sub_cat in sub_cats:
                        words = sub_cat.lower().split(",")
                        presence = [word.strip() in sub for word in words]
                        if all(presence):
                            selections.append(sub_cat)

            motivated_abilities[cat] = selections

        # Add the selected checkboxes to the step4_summary table

        steps_summary_db = StepsSummary("step_data.db")
        steps_summary_db.create_table()
        if steps_summary_db.fetch_data(3, selected_user_id):
            steps_summary_db.update_data(
                3, selected_user_id, json.dumps(motivated_abilities)
            )
        else:
            steps_summary_db.add_data(
                3, selected_user_id, json.dumps(motivated_abilities)
            )
        steps_summary_db.close()

    # Code to process and pass the data to the template goes here
    return render_template(
        "step4_summary.html", data=data, sub_categories=sub_categories, totals=totals
    )
