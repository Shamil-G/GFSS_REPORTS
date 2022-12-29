import db_config as cfg
from util.logger import log
from flask import request
from gfss_reports_parameter import using
import cx_Oracle
# from cx_Oracle import SessionPool
# con = cx_Oracle.connect(cfg.username, cfg.password, cfg.dsn, encoding=cfg.encoding)


def ip_addr():
    if using[0:3] != 'DEV':
        return request.environ.get('HTTP_X_REAL_IP')
    else:
        return request.remote_addr


def init_session(connection, requestedTag_ignored):
    cursor = connection.cursor()
    cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'DD.MM.YYYY HH24:MI'")
    log.debug("--------------> Executed: ALTER SESSION SET NLS_DATE_FORMAT = 'DD.MM.YYYY HH24:MI'")
    cursor.close()


# cx_Oracle.init_oracle_client(lib_dir=cfg.LIB_DIR, config_dir=r"C:\oracle\your_config_dir")
cx_Oracle.init_oracle_client(lib_dir=cfg.LIB_DIR)
_pool = cx_Oracle.SessionPool(cfg.username, cfg.password, cfg.dsn,
                              timeout=cfg.timeout, wait_timeout=cfg.wait_timeout,
                              max_lifetime_session=cfg.max_lifetime_session,
                              encoding=cfg.encoding, min=cfg.pool_min, max=cfg.pool_max, increment=cfg.pool_inc,
                              threaded=True, sessionCallback=init_session)
log.info(f'Пул соединенй БД Oracle создан. Timeout: {_pool.timeout}, wait_timeout: {_pool.wait_timeout}, '
         f'max_lifetime_session: {_pool.max_lifetime_session}, min: {cfg.pool_min}, max: {cfg.pool_max}')


def get_connection():
    if cfg.Debug > 3:
        log.debug("Получаем курсор!")
    return _pool.acquire()


def close_connection(connection):
    _pool.release(connection)


def select(stmt):
    results = []
    mistake = 0
    err_mess = ''
    try:
        with get_connection().cursor() as cursor:
            #log_outcoming.info(f"\nВыбираем данные: {stmt}")
            cursor.execute(stmt)
            recs = cursor.fetchall()
            for rec in recs:
                results.append(rec)
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        mistake = 1
        err_mess = f"Oracle error: {error.code} : {error.message}"
        log.error(f"------select------> ERROR with: {stmt}.")
        log.error(err_mess)
    finally:
        return mistake, results, err_mess


def select_one(stmt, args):
    mistake = 0
    err_mess = ''
    try:
        with get_connection().cursor() as cursor:
            #log_outcoming.info(f"\nВыбираем данные: {stmt}")
            cursor.execute(stmt, args)
            rec = cursor.fetchone()
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        mistake = 1
        err_mess = f"Oracle error: {error.code} : {error.message}"
        log.error(f"------select------> ERROR with: {stmt}.")
        log.error(err_mess)
    finally:
        return mistake, rec, err_mess


def plsql_execute(cursor, f_name, cmd, args):
    try:
        cursor.execute(cmd, args)
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        log.error(f"------execute------> ERROR. {f_name}. IP_Addr: {ip_addr()}, args: {args}")
        log.error(f"Oracle error: {error.code} : {error.message}")


def plsql_proc_s(f_name, proc_name, args):
    with get_connection().cursor() as cursor:
        plsql_proc(cursor, f_name, proc_name, args)


def plsql_func_s(f_name, proc_name, args):
    with get_connection().cursor() as cursor:
        return plsql_func(cursor, f_name, proc_name, args)


def plsql_proc(cursor, f_name, proc_name, args):
    try:
        cursor.callproc(proc_name, args)
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        # log.error(f"-----plsql-proc-----> ERROR. {f_name}. IP_Addr: {ip_addr()}, args: {args}")
        log.error(f"-----plsql-proc-----> ERROR. {f_name}. ARGS: {args}")
        log.error(f"Oracle error: {error.code} : {error.message}")


def plsql_func(cursor, f_name, func_name, args):
    ret = ''
    try:
        ret = cursor.callfunc(func_name, str, args)
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        log.error(f"-----plsql-func-----> ERROR. {f_name}. IP_Addr: {ip_addr()}, args: {args}")
        log.error(f"Oracle error: {error.code} : {error.message}")
    return ret


if __name__ == "__main__":
    log.debug("Тестируем CONNECT блок!")
    con = get_connection()
    log.debug("Версия: " + con.version)
    val = "Hello from main"
    con.close()
    _pool.close()