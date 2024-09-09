from WORKOUT_PROJECT.init_db import db_session
from flask import Flask


app = Flask(__name__)
app.debug = True

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
    
import WORKOUT_PROJECT.index

