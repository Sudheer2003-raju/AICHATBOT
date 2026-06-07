import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from chatbot import get_response

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "aichatbot-secret")

# Predefined questions the bot can ask when requested
QUESTIONS = [
    "What's your experience with Python?",
    "Have you worked with machine learning before?",
    "What AI topics interest you most?",
    "Do you prefer practical examples or theoretical explanations?",
    "Would you like resources or code samples?",
]

@app.route("/")
def home():
    if "username" not in session:
        return redirect(url_for("login"))

    return render_template(
        "index.html",
        username=session["username"],
        chat_history=session.get("chat_history", []),
        openai_enabled=bool(os.getenv("OPENAI_API_KEY")),
    )

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        if not username:
            flash("Please enter a display name to continue.")
            return render_template("login.html")

        session["username"] = username
        session["chat_history"] = []
        session["sequence_active"] = False
        session["sequence_index"] = 0
        return redirect(url_for("home"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/clear_history", methods=["POST"])
def clear_history():
    session["chat_history"] = []
    session["sequence_active"] = False
    session["sequence_index"] = 0
    return jsonify({"status": "ok"})

@app.route("/get_response", methods=["POST"])
def chatbot_response():
    if "username" not in session:
        return jsonify({"error": "Not logged in"}), 401

    user_message = request.json["message"]
    bot_response = get_response(user_message)

    history = session.get("chat_history", [])
    history.append({"sender": "user", "message": user_message})
    history.append({"sender": "bot", "message": bot_response})

    next_question = None
    sequence_complete = False

    # Check if sequence is active
    if session.get("sequence_active", False):
        current_index = session.get("sequence_index", 0)
        next_index = current_index + 1

        if next_index < len(QUESTIONS):
            next_question = QUESTIONS[next_index]
            history.append({"sender": "bot", "message": next_question})
            session["sequence_index"] = next_index
        else:
            sequence_complete = True
            session["sequence_active"] = False

    session["chat_history"] = history

    response_data = {
        "response": bot_response,
        "chat_history": history,
        "next_question": next_question,
        "sequence_complete": sequence_complete
    }

    return jsonify(response_data)


@app.route("/start_sequence", methods=["POST"])
def start_sequence():
    if "username" not in session:
        return jsonify({"error": "Not logged in"}), 401

    session["sequence_active"] = True
    session["sequence_index"] = 0

    history = session.get("chat_history", [])
    first_question = QUESTIONS[0]
    history.append({"sender": "bot", "message": first_question})
    session["chat_history"] = history

    return jsonify({
        "next_question": first_question,
        "sequence_complete": False,
        "chat_history": history
    })


@app.route("/ask_all", methods=["POST"])
def ask_all():
    if "username" not in session:
        return jsonify({"error": "Not logged in"}), 401

    # Append all predefined questions as bot messages
    history = session.get("chat_history", [])
    for q in QUESTIONS:
        history.append({"sender": "bot", "message": q})

    session["chat_history"] = history
    return jsonify({"questions": QUESTIONS, "chat_history": history})

if __name__ == "__main__":
    app.run(debug=True)