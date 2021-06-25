import os
import glob
import shutil


def remove_static_files():
    if os.name == 'nt':
        CLEANUP_FOLDER = os.path.join(os.getcwd(), 'static', 'results')
        shutil.rmtree(CLEANUP_FOLDER)
        os.mkdir(CLEANUP_FOLDER)
    else:
        CLEANUP_FOLDER = os.path.join(os.getcwd(), 'static', 'results', '*')
        files = glob.glob(CLEANUP_FOLDER)
        for f in files:
            os.remove(f)
