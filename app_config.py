from ais_gfss_parameter import using, app_name

if using == 'DEV_WIN':
    BASE = f'C:/Projects/{app_name}'
else:
    BASE = f'/home/ais_gfss/{app_name}'

if using.startswith('DEV_WIN'):
    os = '!unix'
    host = '192.168.5.17'
    debug_level = 3
    port = 8080
else:
    os = 'unix'
    debug_level = 3
    host = 'localhost'
    port = 80

debug = True
LOG_PATH = "logs"