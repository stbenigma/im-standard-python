from datetime import datetime
from IM_DB import parameters

logcount: int = 0
logfile = None


def initlog(pfunc):
    """initializes the logfile for appending (creating if it does not exist)
        sets the logcounter to 0"""
    global logcount, logfile
    logcount = 0
    logfile = open(parameters.logfilepath(), 'a+')
    logfile.write("{}  {}: Model={}  DB={}\n"
                  .format(datetime.now().strftime("%Y-%m-%d %H:%m:%S")
                          ,pfunc
                          ,parameters.odmIMDirec() + parameters.odmModelName() + parameters.odmIMExtension()
                          ,parameters.dbFilePath()))

# initlog

def writelog(pline: str):
    """writes a line to the logfile and increments the logcounter"""
    global logcount, logfile
    if logfile is None:
        raise Exception("Logfile is none in writelog!")
    logcount += 1
    logfile.write("\t{}\n".format(pline))
# writelog

def showmessages(pmsg: str = None):
    """if there are any logentries or a pmsg, writes a showmessages to the console"""
    global logcount, logfile
    if logfile is None:
        raise Exception("Logfile is none in writelog!")
    import __main__
    if pmsg is not None: print("{}:\n  => {}".format(__main__.__file__, pmsg))
    if logcount > 0:
        logfile.close()
        if pmsg is None: print("{}:\n".format(__main__.__file__))
        print("  => {} log entr{} written to {}"
              .format(logcount.__str__(), 'y' if logcount == 1 else 'ies', logfile.name))
# showmessages
