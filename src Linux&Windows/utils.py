# utils.py
import json
import os
import sys

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def load_app_config():
    default = {"enable_dicom_bridge": True}
    try:
        if os.path.exists("app_config.json"):
            with open("app_config.json", "r", encoding="utf-8") as f:
                cfg = json.load(f)
                default.update(cfg)
    except:
        pass
    return default
