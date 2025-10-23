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

@app.route('/chars/<sheet>')
def view_char(sheet):
    if 'user' not in session:
        return redirect(url_for('index'))
    username = session['user']
    path = user_chars_dir(username) / f'{sheet}.json'
    if not path.exists():
        return f'Character "{sheet}" is not found', 404
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return render_template('char.html', data=data, sheet_name=sheet, editable=False)

@app.route('/edit/<name>')
def edit_char(name):
    data = load_char(name)
    if data is None:
        return f'Character "{name}" is not found', 404
    return render_template('edit.html', data=data, name=name, editable=True)

# Ниже добавил Создать/Редактировать/Удалить листы персонажа

def user_chars_dir(username: str):
    path = pathlib.Path(app.root_path) / 'data' / 'chars' / username
    path.mkdir(parents=True, exist_ok=True)
    return path

def load_user_char(username: str, charname: str):
    path = user_chars_dir(username) / f'{charname}.json'
    if not path.exists():
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)
    
def save_user_char(username: str, charname: str, data: dict):
    path = user_chars_dir(username) / f'{charname}.json'
    with open(path, 'w', encoding='utf-8') as f:
        return json.dump(data, f, indent=4, ensure_ascii=False)

def list_user_chars(username: str):
    chars_path = user_chars_dir(username)
    chars = []
    for file in chars_path.glob('*.json'):
        with open(file, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except Exception:
                data = {}
        chars.append({
            'sheet': file.stem,
            'name': data.get('name', '')
        })
    return chars

@app.route('/api/chars', methods=['GET'])
def api_list_user_chars():
    if 'user' not  in session:
        return jsonify(ok=False, error='unauthorized'), 403
    username = session['user']
    return jsonify(ok=True, chars=list_user_chars(username))

@app.route('/api/chars', methods=['POST'])
def api_create_user_char():
    if 'user' not in session:
        return jsonify(ok=False, error='unauthorized'), 403
    data = request.get_json(force=True)
    name = (data.get('name') or '').strip()
    if not name:
        return jsonify(ok=False, error='empty_name'), 400
    username = session['user']
    path = user_chars_dir(username) / f'{name}.json'
    if path.exists():
        return jsonify(ok=False, error='exists'), 409
    template_path = pathlib.Path(app.root_path) / 'data' / 'chars' / 'template.json'
    if not template_path.exists():
        return jsonify(ok=False, error='template_missing'), 500
    with open(template_path, 'r', encoding='utf-8') as f:
        template = json.load(f)
    template['name'] = name
    save_user_char(username, name, template)
    return jsonify(ok=True, message=f'Sheet "{name}" created')

@app.route('/api/chars/<sheet>', methods=['DELETE'])
def api_delete_user_char(sheet):
    if 'user' not in session:
        return jsonify(ok=False, error='unauthorized'), 403
    username = session['user']
    path = user_chars_dir(username) / f'{sheet}.json'
    if not path.exists():
        return jsonify(ok=False, error='not_found'), 404
    path.unlink()
    # os.remove(path)
    return jsonify(ok=True, message=f'Sheet "{sheet}" deleted')

@app.route('/api/chars/<sheet>', methods=['PUT'])
def api_rename_user_char(sheet):
    if 'user' not in session:
        return jsonify(ok=False, error='unauthorized'), 403
    
    data = request.get_json(force=True)
    new_name = data.get('new_name', '').strip()
    if not new_name:
        return jsonify(ok=False, error='empty_new_name'), 400
    
    username = session['user']
    old_path = user_chars_dir(username) / f'{sheet}.json'
    new_path = user_chars_dir(username) / f'{new_name}.json'

    if not old_path.exists():
        return jsonify(ok=False, error='not_found'), 404
    if new_path.exists():
        return jsonify(ok=False, error='exists'), 409
    
    try:
        old_path.rename(new_path)
        return jsonify(ok=True, message=f'Sheet renamed suc renm')
    except Exception as e:
        return jsonify(pk=False, error=str(e)), 500

@app.route('/api/chars/<sheet>', methods=['PATCH'])
def api_update_user_char(sheet):
    if 'user' not in session:
        return jsonify(ok=False, error='unauthorized'), 403

    username = session['user']
    path = user_chars_dir(username) / f'{sheet}.json'

    if not path.exists():
        return jsonify(ok=False, error='not_found'), 404

    try:
        with open(path, 'r', encoding='utf-8') as f:
            current_data = json.load(f)

        updates = request.get_json(force=True)

        def merge_dicts(base, updates):
            if not isinstance(base, dict) or not isinstance(updates, dict):
                return updates
            for key, value in updates.items():
                if isinstance(value, dict) and isinstance(base.get(key), dict):
                    merge_dicts(base[key], value)
                else:
                    base[key] = value
            return base

        updated_data = merge_dicts(current_data, updates)

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(updated_data, f, indent=4, ensure_ascii=False)

        return jsonify(ok=True, message=f'Character "{sheet}" updated')

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify(ok=False, error=str(e)), 500


if __name__ == '__main__':
    app.run(debug=True)