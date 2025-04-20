#!/usr/bin/env python3

import cgi
import cgitb
import json
import os

cgitb.enable()


form = cgi.FieldStorage()
username = form.getvalue("username", "").strip()
email    = form.getvalue("email", "").strip()
password = form.getvalue("password", "").strip()


new_user = {
    "username": username,
    "email": email,
    "password": password   
}


DATA_FILE = "users.json"


if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            users = json.load(f)
        except json.JSONDecodeError:
            users = []
else:
    users = []

users.append(new_user)
with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(users, f, indent=2)


print("Content-Type: text/html\n")
print(f"""
<!DOCTYPE html>
<html>
<head>
  <title>Sign Up Successful</title>
  <link rel="stylesheet" href="styles.css" />
</head>
<body>
   <header>
    <h1>FlashQuiz</h1>
    <nav>
      <a href="index.html" class="active">Home</a>
      <a href="progress.html">Progress</a>
      <a href="signup.html">Sign Up</a>
      <a href="#">Login</a>
    </nav>
  </header>

  <main class="centered-container">
    <section class="form-box">
      <h2>Welcome, {username}!</h2>
      <p>Your account has been created successfully.</p>
      <p><a href="index.html">Click here to log in</a></p>
    </section>
  </main>

  <footer>
    <p>&copy; 2025 FlashQuiz</p>
  </footer>
</body>
</html>
""")
