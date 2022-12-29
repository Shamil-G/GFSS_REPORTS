from gfss_reports_parameter import using, app_name

if using == 'DEV_WIN':
    BASE = f'C:/Projects/{app_name}'
else:
    BASE = f'/home/ais_gfss/{app_name}'

if using.startswith('DEV_WIN'):
    os = '!unix'
    host = 'localhost'
    debug_level = 3
    port = 8080
else:
    os = 'unix'
    debug_level = 3
    host = 'localhost'
    port = 80

debug = True
language = 'ru'
src_lang = 'file'
LOG_PATH = "logs"
LOG_FILE = f'{BASE}/reports_gfss.log'
UPLOAD_PATH = f'{BASE}/reports'
