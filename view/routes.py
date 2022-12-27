from main_app import app, log, cfg
import json
from flask import request


empty_response_save = """
<h2>Hello World</h2>
<p>Maybe Must be used POST method with JSON data</p>
"""

@app.route('/', methods=['POST', 'GET'])
def view_index():
    return empty_response_save, 200, {'Content-Type': 'text/html;charset=utf-8'}

@app.route('/list_reports', methods=['POST', 'GET'])
def view_list_reports():
    if request.method == 'GET':
        reports = { "DIA" : {
                        "rep_01": "test_01",
                        "rep_02": "test_02"
                    },
                   "DMN": {
                        "rep_01": "test_01",
                        "rep_02": "test_02"
                    }
            }
        return reports, 200, {'Content-Type': 'text/json;charset=utf-8'}

