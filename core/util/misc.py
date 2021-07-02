"""
    Core Application Miscellaneous Utility
    core/util/misc.py
"""


def get_file_extension(file_name):
    """ Returns a file extension """
    if isinstance(file_name, str) and len(file_name.split('.')) > 1:
        return file_name.split('.')[-1].lower()
    return None


def get_simpler_datetime(datetime):
    """ Returns a simpler date and time """
    return ':'.join(datetime.split(':')[:2])
