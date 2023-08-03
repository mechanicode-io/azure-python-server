import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SLEEP_DURATION = int(os.environ.get('SLEEP_DURATION'))
    CONNECTION_STRING = os.environ.get('APPLICATIONINSIGHTS_CONNECTION_STRING')
