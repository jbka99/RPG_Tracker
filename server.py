from flask import Flask, jsonify, request, render_template, abort, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import json, os, pathlib

app = Flask(__name__)
app.secret_key = "AnalFuckingDickSucking"

USERS_FILE = pathlib.Path(app.root_path) / "data" / "users.json"

def load_char(name):
    path = os.path.join(app.root_path, 'data', 'chars', f'{name}.json')
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_users():
    if not USERS_FILE.exists():
        return {"users": []}
    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data
    
def save_users(users: dict):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=4, ensure_ascii=False)


def find_user(users: dict, username: str):
    for u in users['users']:
        if u['username'] == username:
            return u
    return None

@app.route("/api/register", methods=["POST"])
def api_register():
    data = request.get_json(force=True)
    username = (data.get("username") or "").strip()
    password = (data.get("password") or "").strip()
    if not username or not password:
        return jsonify(ok=False, error="empty"), 400
    users = load_users()
    if find_user(users, username):
        return jsonify(ok=False, error="exists"), 409
    users["users"].append({
        "username": username,
        "password": generate_password_hash(password)
    })
    save_users(users)
    session["user"] = username
    return jsonify(ok=True)

@app.route('/api/login', methods=["POST"])
def api_login():
    data = request.get_json(force=True)
    username = (data.get("username") or "").strip()
    password = (data.get("password") or "").strip()
    users = load_users()
    u = find_user(users, username)
    if not u or not check_password_hash(u["password"], password):
        return jsonify(ok=False, error="bad_credentials"), 401
    session["user"] = username
    return jsonify(ok=True)

@app.route('/api/logout', methods=["POST"])
def api_logout():
    session.pop("user", None)
    return jsonify(ok=True)

@app.route('/')
def index():
    if 'user' in session:
        return render_template('index.html', logged_in=True, username=session['user'])
    else:
        return render_template('index.html', logged_in=False)
    # return render_template('index.html')

@app.route('/chars/<name>')
def view_char(name):
    data = load_char(name)
    if data is None:
        return f'Character "{name}" is not found', 404
    return render_template('char.html', data=data, name=name, editable=False)

@app.route('/edit/<name>')
def edit_char(name):
    data = load_char(name)
    if data is None:
        return f'Character "{name}" is not found', 404
    return render_template('edit.html', data=data, name=name, editable=True)

if __name__ == '__main__':
    app.run(debug=True)