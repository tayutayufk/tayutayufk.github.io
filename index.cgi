#!/home/ropeproject/local/python/bin/python3
import cgitb
cgitb.enable()

from wsgiref.handlers import CGIHandler
from app import app
CGIHandler().run(app)