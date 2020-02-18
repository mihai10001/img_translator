import os
import glob


def remove_static_files():
    CLEANUP_FOLDER = os.getcwd() + '/static/*'
    files = glob.glob(CLEANUP_FOLDER)
    for f in files:
        os.remove(f)
