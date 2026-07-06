from flask import Flask, render_template, request, session
from questions import questions
import random

app = Flask(__name__)
app.secret_key = "intelliquiz"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/quiz", methods=["POST"])
def quiz():

    name = request.form["name"]
    age = request.form["age"]
    category = request.form["category"]

    session["name"] = name
    session["age"] = age
    session["category"] = category
    session["score"] = 0
    session["question_index"] = 0
    session["wrong_answers"] = []

    selected_questions = random.sample(
        questions[category],
        min(10, len(questions[category]))
    )

    session["selected_questions"] = selected_questions

    return render_template(
        "quiz.html",
        question=selected_questions[0],
        total_questions=len(selected_questions)
    )


@app.route("/result", methods=["POST"])
def result():

    answer = request.form["answer"]

    question_index = session["question_index"]
    selected_questions = session["selected_questions"]

    current_question = selected_questions[question_index]

    if answer == current_question["answer"]:
        session["score"] += 1

    else:
        wrong = session["wrong_answers"]

        wrong.append({
            "question": current_question["question"],
            "your_answer": answer,
            "correct_answer": current_question["answer"]
        })

        session["wrong_answers"] = wrong

    session["question_index"] += 1

    if session["question_index"] < len(selected_questions):

        next_question = selected_questions[
            session["question_index"]
        ]

        return render_template(
            "quiz.html",
            question=next_question,
            total_questions=len(selected_questions)
        )

    score = session["score"]
    total_questions = len(selected_questions)

    percentage = round(
        (score / total_questions) * 100,
        2
    )

    age = int(session["age"])

    if percentage >= 90:
        brain_age = age + 4
        level = "Advanced"

    elif percentage >= 70:
        brain_age = age + 2
        level = "Good"

    elif percentage >= 50:
        brain_age = age
        level = "Average"

    else:
        brain_age = age - 2
        level = "Needs Improvement"

    return render_template(
        "result.html",
        name=session["name"],
        age=session["age"],
        category=session["category"],
        score=score,
        total_questions=total_questions,
        percentage=percentage,
        brain_age=brain_age,
        level=level,
        wrong_answers = session["wrong_answers"],
    )


if __name__ == "__main__":
    app.run(debug=True)