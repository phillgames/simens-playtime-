from flask import Flask, request, render_template
from werkzeug.security import generate_password_hash
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'godot',
    'password': 'password',
    'database': 'godoths'
}

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    score = request.form["score"]
    hashed_password = generate_password_hash(password)

    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        query = "INSERT INTO users (user, pass, score) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, hashed_password, score))
        conn.commit()
        cursor.close()
        conn.close()
        return "redirect(url_for('success'))"
    except Exception as e:
        return f"An error occurred: {e}"

@app.route("/update_score", methods=["POST"])
def update_score():
    username = request.form["username"]
    new_score = request.form["score"]

    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        query = "UPDATE users Set score = %s WHERE user =%s"
        cursor.execute(query, (new_score, username))
        conn.commit()
        cursor.close()
        conn.close()
        return "Score updated successfully"
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)