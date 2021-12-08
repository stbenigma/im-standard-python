import sys
from datetime import datetime
from SSOT_infra import parameters

logcount: int = 0
logfile = None

"""functions to handle a logfile
"""

def initlog(pfunc):
    """initializes the logfile for appending (creating if it does not exist)
        sets the logcounter to 0
        """
    global logcount, logfile
    logcount = 0
    logfile = open(parameters.logfilepath(), 'a+')
    logfile.write("{}  {}: Model={}  DB={}\n"
                  .format(datetime.now().strftime("%Y-%m-%d %H:%m:%S")
                          , pfunc
                          , parameters.odmIMDirec() + parameters.modelName() + parameters.odmIMExtension()
                          , parameters.dbFilePath()))
    return

def writelog(pline: str):
    """writes a line to the logfile and increments the logcounter
    """

    global logcount, logfile
    if logfile is not None:
        logcount += 1
        logfile.write("\t{}\n".format(pline))

    return

def showmessages(pmsg: str = None):
    """
    if there are any log-entries or a pmsg,
    writes a showmessages to the console
    """

    global logcount, logfile
    myfilename = sys.argv[0]
    if logfile is not None:
        if pmsg is not None: print(f"{myfilename}:\n  => {pmsg}")
        if logcount > 0:
            logfile.close()
            if pmsg is None: print(f"{myfilename}:\n")
            plural = lambda cnt: 'y' if cnt == 1 else 'ies'
            print(f"  => {logcount.__str__()} log entr{plural(logcount)} written to {logfile.name}")
    return

