import sys
from pathlib import Path
import argparse

from SSOT_db.IM_JSON import JSModel
from IM_WEB.IM_HTML import svggeneration
from SSOT_infra import removenonchars,argparseparent,nvl

def diagramsvgtofile(jsonfilepath:Path,diagname:str,outfilepath:Path):
    """reads a json file and generates the svg diagram representation
        into the outfile
        outfilepath = None defaults to modelname-diagramname.svg
        """
    jsonmodel = JSModel.readfromfile(pfilename=jsonfilepath)
    diag=jsonmodel.getbyfield(pvalue=diagname,ptype="diagrams")
    assert len(diag)>0, f"Diagram \"{diagname}\" not found in jsonfile \"{str(jsonfilepath)}\""
    diagid = diag[0][0]

    locpath = outfilepath
    if locpath is None:
        locpath = Path(jsonfilepath)
        locpath = locpath.with_name(jsonmodel.modelname()
                                          +"_"
                                          +removenonchars(diagname)
                                            +".svg"
                                          )
    f = open(locpath, "w")
    f.write(svggeneration.renderdiagram(model=jsonmodel, diagid=diagid,
                          lang=jsonmodel.getdefaultlang()))
    f.close()
    print (f"Diagram \"{locpath}\" written.")
    return

def main(psysargs):
    """
    parses sysargs, searches for model and directories and calls
    show version

    :param psysargs:
    :return:
    """
    parser = argparse.ArgumentParser(description='publish svg representation of diagrams')
    parser.add_argument('jsonfilepath', nargs='?',help=f"Path of the jsonfile.")
    parser.add_argument('--name', '-n', dest="name",
                        help=f"Name of diagram to be generated")
    parser.add_argument('--destination', '-d', dest="destination",
                        help=f"Path of generated file. Default <modelname>_<diagramname>.svg")
    parser.add_argument('--version', '-v', action='store_true')
    argparse.Namespace()

    if (len(psysargs) > 0) and ('.py' in psysargs[0]) and ('ipykernel' not in psysargs[0]):
        arguments: argparse.Namespace = parser.parse_args(psysargs[1:])
        myargs = arguments.__dict__
    else:
        # in jupyter environment
        """set myargs with arguments """
    # fi
    if 'version' in myargs and myargs['version']:
        argparseparent.showversion()
        exit(0)

    assert nvl(myargs["name"])!="", "\"name\" (of diagram) must be present"
    assert nvl(myargs["jsonfilepath"])!="", "\"jsonfilepath\" must be present"

    diagramsvgtofile(jsonfilepath=Path(myargs["jsonfilepath"]),
                     diagname=myargs["name"],
                     outfilepath=myargs["destination"])

    return

if __name__ == '__main__':
    main(sys.argv)


