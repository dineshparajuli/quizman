from flask import Flask, jsonify, request
import json
import random
import os

app = Flask(__name__)

def load_questions():
    try:
        file_path = os.path.join(os.path.dirname(__file__), '..', 'questions.json')
        with open(file_path, 'r') as f:
            questions = json.load(f)
        return questions
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return []

@app.route('/api/questions', methods=['GET'])
def get_random_questions():
    questions = load_questions()
    if not questions:
        return jsonify({"error": "Failed to load questions"}), 500
    random_questions = random.sample(questions, min(80, len(questions)))
    # Exclude CorrectAnswer from response to prevent cheating
    safe_questions = [{k: v for k, v in q.items() if k != 'CorrectAnswer'} for q in random_questions]
    return jsonify(random_questions=safe_questions)

@app.route('/api/check_answer', methods=['POST'])
def check_answer():
    data = request.get_json()
    question_text = data.get('question')
    selected_option = data.get('selectedOption')
    if not question_text or not selected_option:
        return jsonify({"error": "Missing question or selected option"}), 400
    questions = load_questions()
    question = next((q for q in questions if q['question'] == question_text), None)
    if not question:
        return jsonify({"error": "Question not found"}), 404
    is_correct = str(question['CorrectAnswer']) == str(selected_option)
    return jsonify({
        "isCorrect": is_correct,
        "correctAnswer": question['CorrectAnswer']
    })

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=os.environ.get('VERCEL') is None)
