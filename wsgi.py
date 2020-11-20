import os

from app import app

def module_exists(module_name):
    try:
        __import__(module_name)
    except ImportError:
        return False
    else:
        return True

# set env variables:
def set_performance_vars():
    os.environ['NUMBA_NUM_THREADS'] = "1"
    os.environ['MKL_NUM_THREADS'] = "1"
    os.environ['OMP_NUM_THREADS'] = "1"
    os.environ['OPENBLAS_NUM_THREADS'] = "1"

set_performance_vars()

if __name__ == "__main__":
    app.run()