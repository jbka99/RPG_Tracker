from flask import Flask, jsonify, request, render_template
import json

app = Flask(__name__, static_folder='', template_folder='')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/character', methods=['GET', 'POST'])
def character():
    with open('RPG_project/character.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    if request.method == 'POST':
        new_data = request.get_json()
        if new_data.get('level_up'):
            data['level'] += 1
        elif new_data.get('level_down'):
            data['level'] -= 1
        with open('RPG_project/character.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


    if request.method == 'POST':
        new_data = request.get_json()
        if new_data.get('stat_synt_up'):
            data['stats'["Синтаксис"]] += 1
        elif new_data.get('stat_synt_down'):
            data['stats'["Синтаксис"]] -= 1
        with open('RPG_project/character.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    with open('RPG_project/character.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    return jsonify(data)

# @app.route('/get')
# def get_data():
#     with open('character.json', 'r', encoding='utf-8') as f:
#         data = json.load(f)
#     return jsonify(data)

# @app.route('/update', methods=['POST'])
# def upd_data():
#     new_data = request.get_json()
#     with open('character.json', 'r', encoding='utf-8') as f:
#         data = json.load(f)
#     data.update(new_data)
#     with open('character.json', 'w', encoding='utf-8') as f:
#         json.dump(data, f, indent=4, ensure_ascii=False)
    # return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)