import os
import sys

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for cx_freeze"""
    base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)