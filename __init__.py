from ais_gfss_parameter import using, app_name
from flask import Flask
from util.logger import log


app = Flask(__name__)
app.secret_key = 'IAS GFSS Delivery secret key: 232lk;lf09ut;ih;gs'

log.info(f"__INIT MAIN APP for {app_name} started")
print("__INIT MAIN APP__ started")