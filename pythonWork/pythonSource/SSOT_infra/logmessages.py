from datetime import datetime

from SSOT_infra import parameters
from SSOT_infra.translateprompt import plural

logcount: int = 0
logfile = None


def nop_trap(str):
    pass


logtrap = nop_trap

"""functions to handle a logfile.

    Uses parameters.py for locations and names
"""


def initlog(pmodulename: str):
    """initializes the logfile for appending (creating if it does not exist) for the module pmodulename
        sets the logcounter to 0
        """
    global logcount, logfile, logtrap
    logcount = 0
    logfile = open(parameters.logfilepath(), 'a+')
    log_line = "{}  {}: Model={}  DB={}\n".format(datetime.now().strftime("%Y-%m-%d %H:%m:%S")
                                                  , pmodulename
                                                  ,
                                                  parameters.odmIMDirec() + parameters.modelName() + parameters.odmIMExtension()
                                                  , parameters.dbFilePath())
    logfile.write(log_line)
    logtrap(log_line)

    return


def writelog(pline: str):
    """writes a line to the logfile and increments the logcounter

        Does nothing if the log was not initialized
    """
    global logcount, logfile, logtrap

    logtrap(pline)

    if logfile is not None and not logfile.closed:
        logcount += 1
        logfile.write("\t{}\n".format(pline))

    return


def showmessages(pmsg: str = None):
    """
    if there are any log-entries or a pmsg,
    writes a showmessages to the console
    """

    global logcount, logfile
    myfilename = __file__
    if logfile is not None:
        print(f"{myfilename}:")
        if pmsg is not None: print(f" => {pmsg}")
        if logcount > 0:
            logfile.close()
            print(f"  => {logcount.__str__()} log entr{plural('y', logcount)} written to {logfile.name}")
    return
