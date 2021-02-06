import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = 1
    DEVELOPMENT = True
    TESTING = True
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
