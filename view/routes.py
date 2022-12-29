from main_app import app, log, cfg
import json
from flask import render_template, url_for, session, flash, request,  Response, redirect, g, make_response
from flask_login import login_required, current_user, logout_user
from util.utils import *
from model.model_login import *
from model.set_report import set_dep, get_deps, get_grps, set_grp, get_reports


empty_response_save = """
<h2>Hello World</h2>
<p>Maybe Must be used POST method with JSON data</p>
"""

deps = {}
dict_deps = {}
list_grps = []
list_reports = []

@app.route('/', methods=['POST', 'GET'])
def view_index():
    global deps
    global dict_deps
    global list_reports

    if len(deps) == 0:
        deps = get_deps()
        dict_deps = dict(deps)
    log.info(f'VIEW INDEX. DEPS: {deps}')
    current_dep = ''
    current_grp = ''
    if 'current_dep' in session:
        current_dep = dict_deps.get(session['current_dep'])
        if 'current_grp' in session:
            current_grp = session['current_grp']
    log.info(f'VIEW INDEX. CURRENT_GRP: {current_grp}, LIST REPORTS: {list_reports}')
    return render_template("index.html", deps=deps, grps=list_grps, list_reports=list_reports, current_dep=current_dep, current_grp=current_grp)


@app.route('/set-dep/<int:num_dep>')
def view_set_dep(num_dep):
    global list_grps
    set_dep(num_dep)
    results = get_grps()
    list_grps = []
    session.pop("current_grp", None)
    for grp in results:
        list_grps.append(grp[0])
    log.info(f'VIEW SET DEP. GROUPS: {list_grps}')
    return redirect(url_for('view_index'))


@app.route('/set-grp/<string:num_grp>')
def view_set_grp(num_grp):
    global list_reports
    set_grp(num_grp)
    list_reports=get_reports()
    log.info(f'VIEW SET GRP. CURRENT_GRP: {num_grp}, LIST REPORTS: {list_reports}')
    return redirect(url_for('view_index'))


@app.route('/all-deps')
def view_all_deps():
    if 'current_dep' in session:
        session.pop('current_dep', None)
    return redirect(url_for('view_index'))


@app.route('/list-reports', methods=['POST', 'GET'])
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

