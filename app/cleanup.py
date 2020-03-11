import os
import glob
import shutil


def remove_static_files():
    CLEANUP_FOLDER = os.path.join(os.getcwd(), 'static', 'images')
    files = glob.glob(CLEANUP_FOLDER)
    for f in files:
        os.remove(f)


def remove_static_files_win():
    CLEANUP_FOLDER = os.path.join(os.getcwd(), 'static', 'images')
    shutil.rmtree(CLEANUP_FOLDER)
