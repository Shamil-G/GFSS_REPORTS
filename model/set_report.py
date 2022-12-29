from db.connect import select
from flask import session
from main_app import log



def get_deps():
    log.info(f'GET_DEPS...')
    err, results, msg = select('select id_dep, dep_name from rfld_list_dep order by id_dep')
    if err == 0:
       return results
    return None
    
def get_grps():
    log.info(f'GET_GRPS...')
    err, results, msg = select(f"select unique id_grp from rflr_list_reports where id_dep = {session['current_dep']} order by id_grp")
    if err == 0:
        log.info(f'GET GRPS. TYPE: {type(results)}, RESULTS: {results}')
        return results
    return None


def get_reports():
    results = []
    stmt = f"select id_rep, rep_name, p_exec from rflr_list_reports where id_dep = {session['current_dep']} and id_grp='{session['current_grp']}' order by id_grp"
    err, results, msg = select(stmt)
    #if err == 0:
    #    for rep in results:
    #        list_reports.extend(rep)
    log.info(f'GET REPORTS: {results}, err: {err}, msg: {msg} STMT={stmt}')
    return results


def set_dep(num_dep: int):
    log.info(f'SELECT_DEP. NAME_DEP: {num_dep}')
    session['current_dep'] = num_dep

def set_grp(num_grp: str):
    log.info(f'SELECT_DEP. NAME_DEP: {num_grp}')
    session['current_grp'] = num_grp
