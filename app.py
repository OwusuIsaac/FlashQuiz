#!/usr/bin/env python3
import os
import json
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from dotenv import load_dotenv
from google import genai

# Load .env
load_dotenv()
API_KEY = os.getenv('GEMINI_API_KEY')
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set in environment")

# Initialize Gemini client
client = genai.Client(api_key=API_KEY)

# Flask setup
app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.getenv('SECRET_KEY', os.urandom(24).hex())

# Simple user-store (JSON file) and progress in session
DATA_FILE = 'users.json'

def load_users():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            try: return json.load(f)
            except: return []
    return []

def save_users(users):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2)

# Routes
@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password'].strip()
        users = load_users()
        users.append({'username': username, 'email': email, 'password': password})
        save_users(users)
        session['username'] = username
        return redirect(url_for('home'))
    return render_template('signup.html')

@app.route('/', methods=['GET','POST'])
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        for u in load_users():
            if u['username'] == username and u['password'] == password:
                session['username'] = username
                return redirect(url_for('home'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/home', methods=['GET','POST'])
def home():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        topic      = request.form['topic'].strip()
        context    = request.form['context'].strip()
        difficulty = request.form['difficulty']
        qformat    = request.form['format']
        num_q      = int(request.form['numQuestions'])

        prompt = (
            f"Generate exactly {num_q} quiz items on '{topic}' at '{difficulty}' difficulty, "
            f"format '{qformat}'."
            + (f" Context: '{context}'." if context else "")
            + " DO NOT wrap in code fences or add explanations; "
            + "return only the JSON object matching this schema:\n"
            + '{"questions":[{"question":string,"options":[string],"answer":string}]}'
        )

        resp = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=[prompt]
        )

        raw = resp.text.strip()
        # strip fences
        if raw.startswith("```"):
            raw = raw.split("```",2)[1].strip()
        # extract JSON
        start = raw.find("{")
        end   = raw.rfind("}") + 1
        json_blob = raw[start:end]

        try:
            quiz_data = json.loads(json_blob)
        except json.JSONDecodeError:
            app.logger.error("Raw AI output:\n%s", resp.text)
            return render_template('home.html',
                                   error='Failed to parse AI response; check server logs.')

        # everything’s good
        session['quiz_data'] = quiz_data
        session['topic'] = topic
        return redirect(url_for('quiz'))

    return render_template('home.html')

       

@app.route('/quiz')
def quiz():
    if 'username' not in session or 'quiz_data' not in session:
        return redirect(url_for('home'))
    return render_template('quiz.html', quiz_data=session['quiz_data'])

@app.route('/results', methods=['GET','POST'])
def results():
    if 'username' not in session or 'quiz_data' not in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        data = request.get_json()
        quiz_data = session['quiz_data']
        questions = quiz_data.get('questions', [])
        score = 0
        missed = []
        print("data: ", data)
        print("q: ", questions)
        for i, q in enumerate(questions):
            ans = data['answers'][i].strip().lower()
            if ans == q['answer'].strip().lower():
                score += 1
            else:
                missed.append({'question': q['question'], 'answer': q['answer']})
        # Save to session progress
        prog = session.get('progress', [])
        prog.append({'date': __import__('datetime').date.today().isoformat(), 'topic': session.get('topic',''), 'score': score, 'total': len(questions)})
        session['progress'] = prog
        return jsonify({'score': score, 'total': len(questions), 'missed': missed})
    # GET use client-side sessionStorage fallback
    return render_template('results.html')

@app.route('/progress')
def progress():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('progress.html', progress=session.get('progress', []))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500, debug=True)
