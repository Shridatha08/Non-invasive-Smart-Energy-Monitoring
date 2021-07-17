# app.py

from werkzeug.middleware.dispatcher import DispatcherMiddleware # use to combine each Flask app into a larger one that is dispatched based on prefix
from flask_1 import app as flask_app_1
from flask_2 import app as flask_app_2
# from flask_3 import app as flask_app_3
# from flask_4 import app as flask_app_4
from flask_0 import app as flask_app_0

application = DispatcherMiddleware(flask_app_0, {
    '/flask_app_0': flask_app_0,
    '/flask_app_1': flask_app_1,
    '/flask_app_2': flask_app_2,
#     '/flask_app_3': flask_app_3,
#     '/flask_app_4': flask_app_4,
})
