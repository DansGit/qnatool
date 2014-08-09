# Various functions that don't seem to fit anywhere else
import os

def valid_dir(path):
    """Checks if the given str is a valid path to a dir that exists."""

    if not os.path.exists(path):
        print 'ERROR: "{}" does not exist'.format(path)
        return False
    elif not os.path.isdir(path):
        print 'ERROR: "{}" is not a directory'.format(path)
        return False
    else:
        return True
