import os
import sys


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def get_user_data_dir():
    base = os.path.join(
        os.path.expanduser("~"),
        "Library",
        "Application Support",
        "BKcloud"
    )
    os.makedirs(base, exist_ok=True)
    return base


def user_json_path(filename):
    return os.path.join(get_user_data_dir(), filename)
