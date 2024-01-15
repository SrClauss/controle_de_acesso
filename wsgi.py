from flask import Flask, request
from tinydb import TinyDB

db = TinyDB('db.json')
error_table  = db.table('error')
scripts_table = db.table('scripts')

app = Flask(__name__)

@app.route('/send_error', methods=['POST'])
def script_info():
    data = request.get_json()
    error_table.insert(data)
    return {'Message': 'Sucess'}


@app.route('/errors', methods=['GET'])
def get_scripts_info():
    return error_table.all()


@app.route('/', methods=['GET'])
def get_scripts_list():
    return scripts_table.all()


@app.route('/save_script', methods=['POST'])
def save_script():
    data = request.get_json()
    scripts_table.insert(data)
    return {'Message': 'Sucess'}


@app.route('/activate_script', methods=['PUT'])
def activate_script(script_id):
    scripts_table.update({'active': True}, doc_ids=[script_id])
    return {'Message': 'Sucess'}

@app.route('/deactivate_script', methods=['PUT'])
def deactivate_script(script_id):
    scripts_table.update({'active': False}, doc_ids=[script_id])
    return {'Message': 'Sucess'}

@app.route('/get_script_status', methods=['GET'])
def get_script_status(script_id):
    script = scripts_table.get(doc_id=script_id)
    return script['active']
    

if __name__ == '__main__':
    app.run()
