"""
    Core Application Objects Utility
    core/util/objects.py
"""

from crum import get_current_user


def get_file_extension(file_name):
    """ Returns a file extension """
    if isinstance(file_name, str) and len(file_name.split('.')) > 1:
        return file_name.split('.')[-1].lower()
    return None


def save_user_attributes(obj, created_by_field_name='created_by', updated_by_field_name='updated_by'):
    ''' Save user-related attributes of the object '''
    user = get_current_user()
    if user is not None and user.pk is None:
        user = None

    if user is not None:
        if obj.id is None:
            if isinstance(created_by_field_name, str):
                exec('obj.{} = user'.format(created_by_field_name))

        if isinstance(updated_by_field_name, str):
            exec('obj.{} = user'.format(updated_by_field_name))
