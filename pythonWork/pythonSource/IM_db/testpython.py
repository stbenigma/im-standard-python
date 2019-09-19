import os
import pathlib
import sys

current_dir = pathlib.Path(__file__).parent
current_file = pathlib.Path(__file__)
def main():
    print("Testpython main")
    #os.chdir(os.path.dirname(__file__))
    print("getcwd=",os.getcwd())
    print('dirname=',os.path.dirname(__file__))
    print('name=',__name__)

    print ('current_dir = ',pathlib.Path(__file__).parent)
    print('file=',__file__)
    print('current_file = ',pathlib.Path(__file__))

    print(sys.argv)
# end main

if (__name__ == '__main__'):
        main()