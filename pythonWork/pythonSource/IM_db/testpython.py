import os,re
from pathlib import Path
import sys,inspect
from IM_DB import parameters


current_dir = Path(__file__).parent
current_file = Path(__file__)
def main(arg1):
    print("Testpython main")
    print('inspect=',os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
    #os.chdir(os.path.dirname(__file__))
    print("getcwd=",os.getcwd())
    print('dirname=',os.path.dirname(__file__))
    print('name=',__name__)
    print('arg1=',arg1)

    print ('current_dir = ',Path(__file__).parent)
    print('file=',__file__)
    print('current_file = ',Path(__file__))

    print(sys.argv)
    home=Path.home()
    docu = Path(str(home)+'/Documents')
    print ("Home=",home,docu.is_dir())


#    config = configparser.RawConfigParser()
#    config.read('/Users/stb/Documents/Projekte/FYAYC_intern/gitHub/TestModell/IM_ATTR_FYAYC.params')
#    alle  = dict((x,config['DEFAULT'][x].strip("'"+'"')) for  x in config['DEFAULT'])
#    print (alle)
    print("split "+'/a/bdfdf/cd/'[0:len('/a/bdfdf/cd/')-len('cd/')])
    parameters.liesparamfile()

# end main

if (__name__ == '__main__'):
    arg1= None if len(sys.argv) < 2 else sys.argv[1]
    main(arg1)