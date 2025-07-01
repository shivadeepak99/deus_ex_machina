import os

def check_python_installation():
    try:
        import sys
        print("Python is already installed.")
    except ImportError:
        print("Python is not installed. Installing now...")
        os.system('python --version')

check_python_installation()