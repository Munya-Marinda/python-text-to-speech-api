import os
import sys

# Set the path to your application
INTERP = os.path.expanduser("~/venv/bin/python")
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.append(os.getcwd())

from app.main import app as application  # noqa