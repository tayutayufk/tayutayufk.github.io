import cgitb
cgitb.enable()

from wsgiref.handlers import CGIHandler
from appFlask import app
CGIHandler().run(app)