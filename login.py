#!/usr/bin/env python3

import cgi
import cgitb
import json
import os

cgitb.enable()

# Get form data
form = cgi.FieldStorage()
username = form.getvalue("username", "").strip()
password = form.getvalue("password", "").strip()

DATA_FILE = "users.json"

# Load users data
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            users = json.load(f)
        except json.JSONDecodeError:
            users = []
else:
    users = []

# Check if user exists and password matches
user_found = False
for user in users:
    if user["username"] == username and user["password"] == password:
        user_found = True
        break

# Output response
print("Content-Type: text/html\n")
if user_found:
    print(f"""
    <!DOCTYPE html>
    <html>
    <head>
      <title>Login Successful</title>
      <link rel="stylesheet" href="styles.css" />
    </head>
    <body>
      <header>
        <h1>FlashQuiz</h1>
        <nav>
          <a href="index.html" class="active">Login</a>
          <a href="signup.html">Sign Up</a>
        </nav>
      </header>

      <main class="centered-container">
        <section class="form-box">
          <h2>Welcome back, {username}!</h2>
          <p>Login successful. <a href="home.html">Go to Home</a></p>
        </section>
      </main>

      <footer>
        <p>&copy; 2025 FlashQuiz</p>
      </footer>
    </body>
    </html>
    """)
else:
    print(f"""
    <!DOCTYPE html>
    <html>
    <head>
      <title>Login Failed</title>
      <link rel="stylesheet" href="styles.css" />
    </head>
    <body>
      <header>
        <h1>FlashQuiz</h1>
        <nav>
          <a href="index.html" class="active">Login</a>
          <a href="signup.html">Sign Up</a>
        </nav>
      </header>

      <main class="centered-container">
        <section class="form-box">
          <h2>Login Failed</h2>
          <p>Incorrect username or password. <a href="signup.html">Try Again</a></p>
        </section>
      </main>

      <footer>
        <p>&copy; 2025 FlashQuiz</p>
      </footer>
    </body>
    </html>
    """)
