from flask import Flask, jsonify, request, render_template, abort
import json, os

app = Flask(__name__)
#static_folder='', template_folder=''

def load_character(name):
    path = os.path.join(app.root_path, 'data', 'chars', f'{name}.json')
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chars/<name>')
def view_char(name):
    data = load_character(name)
    if data is None:
        return f'Character "{name}" is not found', 404
    return render_template('char.html', data=data, name=name, editable=False)

@app.route('/edit/<name>')
def edit_char(name):
    data = load_character(name)
    if data is None:
        return f'Character "{name}" is not found', 404
    return render_template('edit.html', data=data, name=name, editable=True)

if __name__ == '__main__':
    app.run(debug=True)