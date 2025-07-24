from flask import Flask, jsonify
import json
import random
import os

app = Flask(__name__)

def load_questions():
    try:
        # Load questions from JSON file
        file_path = os.path.join(os.path.dirname(__file__), 'questions.json')
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
    return jsonify(safe_questions)

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=os.environ.get('VERCEL') is None)
