from flask import Flask, request
import requests
from tinydb import TinyDB, Query

db = TinyDB('db.json')


app = Flask(__name__)


prodution = False
url = "https://x9s3hsdp44.us-east-1.awsapprunner.com/" if prodution else "http://192.168.1.6:8080"


"""
{
    "script_id": "script_id",
    "activate": true,
    "errors": [
        {
            "error_list": {
                "datetime": "YYYY-MM-DDTHH:MM:SS.ssssss±hh:mm",
                "errors": [
                    "error_message1",
                    "error_message2",
                    "error_message3"
                ]
            }
        }, 
        {
            "error_list": {
                "datetime": "YYYY-MM-DDTHH:MM:SS.ssssss±hh:mm",
                "errors": [
                    "error_message1",
                    "error_message2",
                    "error_message3"
            }
        }
    ]
}

"""

@app.route("/", methods=['GET'])
def get_scripts_list():
    return db.all(), 200


@app.route("/get_script/<script_id>", methods=['GET'])
def get_script(script_id):
    if not db.search(Query().script_id == script_id):
        return "{\"message\": \"script not found\"}", 404
    return db.search(Query().script_id == script_id)[0], 200

@app.route("/save_script", methods=['POST'])
def save_script():
    body = request.get_json()
    script_exists = db.search(Query().script_id == body['script_id'])
    print(script_exists)
    if script_exists:
        return "{\"message\": \"script already exists\"}", 409
    db.insert(body)
    return body, 200
@app.route("/delete_script/<script_id>", methods=['DELETE'])
def delete_script(script_id):
    scripts = db.search(Query().script_id == script_id)
    if scripts == []:
        return "{\"message\": \"script not found\"}", 404
    db.remove(Query().script_id == script_id)
    return "{\"message\": \"script deleted\"}", 204

@app.route("/activate_script/<script_id>", methods=['PUT'])
def activate_script(script_id):
    script = db.search(Query().script_id == script_id)
    if not script:
        return "{\"message\": \"script not found\"}", 404
    if script[0]['activate']:
        return "{\"message\": \"script already activated\"}", 409
    script[0]['activate'] = True
    db.update(script[0], Query().script_id == script_id)
    return script[0], 200

@app.route("/deactivate_script/<script_id>", methods=['PUT'])
def deactivate_script(script_id):
    script = db.search(Query().script_id == script_id)
    if not script:
        return "{\"message\": \"script not found\"}", 404
    if not script[0]['activate']:
        return "{\"message\": \"script already deactivated\"}", 409
    script[0]['activate'] = False
    db.update(script[0], Query().script_id == script_id)
    return script[0], 200
@app.route("/send_errors/<script_id>", methods=['PUT'])
def send_errors(script_id):
    body = request.get_json()
    script = db.search(Query().script_id == script_id)
    if not script:
        return "{\"message\": \"script not found\"}", 404
    script[0]['errors'].append(body)
    db.update(script[0], Query().script_id == script_id)
    return script[0], 200

if __name__ == "__main__":
    app.run()