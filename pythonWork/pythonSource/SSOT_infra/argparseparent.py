import argparse
import os

from SSOT_infra import parameters,Parameter

"""argparse, creates a parentclass for argumentsparsing of common SSOT-arguments
"""

_parentparser = argparse.ArgumentParser(add_help=False)
langlist = ','.join(Parameter.SUPPORTEDLANGUAGES.keys())
_parentparser.add_argument('--modellanguage', '-ml', dest="modellanguage",
                           help=f"shortname of the main model language. Possible values: " +
                                f"{langlist}. Default 'en' ")
_parentparser.add_argument('--languages', '-l', dest="languages",
                           help=f"languages used in this model . Possible value: list of " +
                                f"{langlist} . Default 'en' ")
_parentparser.add_argument('--logfile', '-log', dest='logfile',
                           help=f"Path for logfile. Default: ./<modelname>{Parameter.LOGFILEEXTENSION}")
_parentparser.add_argument('--modelname', '-m', dest='modelname')
_parentparser.add_argument('--paramfile', '-p', dest='paramfile',
                           help=f"Parameterfile for modelenvironent. "
                                + "Default: ./<modelname>{Parameter.PARAMFILEEXTENSION}")
_parentparser.add_argument('--version', '-v', action='store_true')
_parentparser.add_argument('--unittest', action='store_true', dest='unittest',
                           help=argparse.SUPPRESS)  # for testing purposes only


def parentparser():
    return _parentparser


def argnotnone(pargument, parguments):
    return pargument in parguments and parguments[pargument] is not None


def argisnone(pargument, parguments):
    return not argnotnone(pargument, parguments)


def checkmodelandparam(parguments):
    if not (argnotnone('modelname', parguments) or argnotnone('modelfilepath', parguments) or argnotnone('destination', parguments)):
        print("modelname or modelfilepath or destination must be given")
        exit(1)

def showversion():
    print(f"Versions: Tool: {parameters.toolversion()}     DB: {parameters.expecteddbversion()}")

def fillssotdefaults(pcurrentdir, parguments):
    """resolves the SSOT- and ODM-defaults for common arguments
        parguments : dict of parameters
    """

    # not yet relevant: later-> arguments.dbtype.lower()
    parguments['dbtype'] = Parameter.SQLITE
    # resolve default settings
    if argnotnone('paramfile', parguments):
        if not os.path.isfile(parguments['paramfile']):
            print(f"no such file: {parguments['paramfile']}")
            exit(1)
    if argnotnone('modelname', parguments):
        if argisnone('logfile', parguments):
            parguments['logfile'] = os.path.join(pcurrentdir,
                                                 parguments['modelname'] + Parameter.LOGFILEEXTENSION)

    if argisnone('languages', parguments):
        parguments['languages'] = None if argisnone('modellanguage',parguments) else parguments['modellanguage']
    if argnotnone('modellanguage', parguments) and argnotnone('languages', parguments) and (
            parguments['modellanguage'] not in parguments['languages']):
        parguments['languages'] += ',' + parguments['modellanguage']
