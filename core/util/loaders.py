"""
    Core Application Loaders UStility
    core/util/loaders.py
"""

import pathlib


def load_project_path():
    ''' Load project path '''
    project_path = str(pathlib.Path().absolute()).replace('\\', '/') + '/'

    if project_path == '/':
        return str()
    return project_path
