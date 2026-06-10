import os

from credentials import delete_credentials
from session import session_path


def cmd_logout(_args):
    delete_credentials()
    if os.path.exists(session_path):
        os.remove(session_path)
    print("Logged out. Saved credentials and session removed.")
    print("You will be asked for your username and password on next run.")
