from datetime import datetime
from SSOT_infra.translateprompt import plural
from pathlib import Path

logcount: int = 0
logfile = None


def nop_trap(instr):
    pass

logtrap = nop_trap

"""functions to handle a logfile.

    Uses parameters.py for locations and names
"""


def initlog(pmodulename: str,plogfilepath=None):
    """initializes the logfile for appending (creating if it does not exist) for the module pmodulename
        sets the logcounter to 0
        """
    global logcount, logfile, logtrap
    logcount = 0
    log_line = f"""{datetime.now().strftime("%Y-%m-%d %H:%m:%S")}  {pmodulename}\n"""
    if plogfilepath is not None:
        logpath = plogfilepath
    else:
        logpath = None
    if logpath is not None:
        Path(logpath).parent.mkdir(exist_ok=True)
        logfile = open(logpath, 'a+')
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

def closelog():
    global logfile
    if logfile is not None:
        logfile.close()
        logfile = None


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
            print(f"  => {logcount.__str__()} log entr{plural('y', logcount)} written to {logfile.name}")
        closelog()
    return
