# FlashQuiz App

An interactive flashcard quiz web application built with Flask and Google Gemini AI.

## Features
- User Sign Up / Login
- Dynamic quiz generation using Gemini 2.0 Flash model
- Quiz taking and scoring
- Progress tracking and review
- Simple and clean front-end

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/Yonathan-Wagaye/flashquiz.git
cd flashquiz
```

### 2. Create and activate virtual env
python3 -m venv flashQuiz
source flashQuiz/bin/activate  # On macOS/Linux
flashQuiz\\Scripts\\activate   # On Windows


### 3. Install the necessary required packages
pip freeze > requirements.txt or
pip install -r requirements.txt

### 4. Create .env file in the root directory 
flashquiz/
├── app.py
├── requirements.txt
├── README.md
├── .env <- here is your .env file
├── users.json
├── static/
│   ├── styles.css
│   └── scripts.js
└── templates/
    ├── home.html
    ├── login.html
    ├── signup.html
    ├── progress.html
    ├── quiz.html
    └── results.html

### 5, add the api key to your .env file 
GEMINI_API_KEY=AIzaSyAfQuBfJJPaZG567UrNYoJKxGU-bUZpE4k

### 6. Run application
export FLASK_APP=app.py
flask run --host=0.0.0.0 --port=5000


