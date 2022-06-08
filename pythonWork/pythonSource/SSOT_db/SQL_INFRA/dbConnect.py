import logging
import sqlite3
from contextlib import closing

from SSOT_infra import parameters
from SSOT_db.IM_OBJECTS import Language

""" create database and connect to it
    """

#global db connection used for all DML statements
myDbConn: sqlite3.Connection = None
#db version read from database view dbversion
actualdbversion = {}
opendbs = []

def push():
    global opendbs
    """pushes the current connection (myDbConn)
       and resets myDbConn to None
       if myDbConn is empty, nothing is done  
       """
    if myDbConn is not None:
        opendbs.append(myDbConn)
        setdbcon(None)
    return

def pop ()->sqlite3.Connection:
    global opendbs
    """ if myDbConn is open, close it
        returnvalue and myDbConn = None if stack is empty
       if not, connection from stack is set to myDbConn and returned
       """
    if isopenDB():
        closeDB()
    actconn = None if (len(opendbs)==0) else opendbs.pop()
    setdbcon(actconn)
    return actconn

def resetconnstack():
    """empties connection stack and closes all connections if still open
       should only be used in testing
    """
    global opendbs
    while len(opendbs)>0:
        opendbs.pop()
    return


def openDBbasic(pfilepath, pfks='ON') -> sqlite3.Connection:
    """ opens the db pfilepath
    """
    try:
        locconn = sqlite3.connect(pfilepath)
        setdbcon(locconn)
        setversion()
    except Exception as exp:
        raise exp
    makedbsafe(pdbcon=getdbcon(),pfks=pfks)
    return getdbcon()

def makedbsafe(pdbcon,pfks='ON'):
    pdbcon.execute(f"PRAGMA foreign_keys = {pfks}")
    pdbcon.execute("PRAGMA main.cache_size = -2000")
    return


def opendDB4DDL(pfilepath, pfks="OFF") -> sqlite3.Connection:
    """ creates a database and opens it.
     by default checking is off as I want to do DDL
     """
    return openDBbasic(pfilepath, pfks=pfks)


def openDB(pfilepath, pfks='ON',pversioncheck=True):
    """opens the database pfilepath
    pfks OFF -> no checks enabled (for DDL)
        on -> checks enabled (for DML)
    checks the version and guarantees matching with version-file
    """
    conn = openDBbasic(pfilepath=pfilepath, pfks=pfks)
    if pversioncheck:
        checkversion()
    return conn


def closeDB():
    """ closes open DB and resets the global db-connector
    """
    getdbcon().close()
    setdbcon(None)
    return

def checkson():
    getdbcon().execute(f"PRAGMA foreign_keys = 1")

def isopenDB():
    """if the global db for my environment open?
    """
    return getdbcon() is not None


def getDBname():
    """returns the name of the current DB"""
    cursor = getdbcon().cursor()
    cursor.execute("PRAGMA database_list;")
    curr_table = cursor.fetchall()
    return curr_table[0][2]


def setdbcon(pconn):
    """sets the global db connection to pconn"""
    global myDbConn
    myDbConn = pconn
    return


def getdbcon():
    """gets the global db connection"""
    global myDbConn
    return myDbConn


def readversion(pconn):
    """returns the current version and installation date
    from the connection pconn
    {"version": <version>, "installdate": <installationdate>}
    """
    cursor = pconn.cursor()
    try:
        cursor.execute("select * from dbversion")
        curr_table = cursor.fetchall()
    except Exception as e:
        curr_table = [[None, None]]
    # try
    return {"version": curr_table[0][0]
        , "installdate": curr_table[0][1]
            }


def checkversion():
    """compares the expected db version (stored in parameters) with
    the currently opend db-Version
    raises exception if they mismatch
    """
    actversion, expversion = readversion(getdbcon())['version'], parameters.expecteddbversion()
    if actversion is not None and (actversion != expversion):
        raise Exception(f"DB-Versions expected {expversion}, DB-version found {actversion}")
    return


def setversion():
    """sets the global actualdbversion with the value out the database
    """
    global actualdbversion
    actualdbversion = readversion(getdbcon())
    return


def getversion():
    """return the version of the actually open DB
    """
    global actualdbversion
    if actualdbversion["version"] is None:
        setversion()
    return actualdbversion["version"]


def read_git_revision(connection = None):
    """@:return The git revision stored in the view [gitrevision]
    or '<unknown>' if the view does not exist
    """
    if connection is None:
        connection = getdbcon()
    assert isinstance(connection, sqlite3.Connection)
    try:
        with closing(connection.cursor()) as cursor:
            cursor.execute("select * from [gitrevision]")
            curr_table = cursor.fetchall()
    except sqlite3.Error as e:
        logging.warning(f"Cannot read git revision, returning '<unknown>'. Reason: {e}")
        curr_table = [['<unknown>']]
    # try
    return curr_table[0][0]


def write_git_reversion(version: str, connection = None):
    """Create view 'gitrevision' holding only the git revision"""
    assert len(version) > 0
    if connection is None:
        connection = getdbcon()
    assert isinstance(connection, sqlite3.Connection)
    safe_version = version.replace("'", "''")
    connection.execute("DROP VIEW IF EXISTS [gitrevision];")
    statement = f"CREATE VIEW [gitrevision] AS SELECT '{safe_version}' AS [revision];"
    connection.execute(statement)

def getconnlangparameters():
    assert isopenDB()
    deflang = Language.getdefaultlang().lang_iso_code2
    langs = Language.getlanguagecodes()
    return (deflang,langs)


# def getdblangparameters(pfilepath):
#     with closing(openDBbasic(pfilepath)) as conn:
#         deflang,langs = getconnlangparameters()
#         parameter.modelLang(newval=deflang)
#         parameter.languages(newval=','.join(langs))
#     return

def connectmemorydb()->sqlite3.Connection:
    return sqlite3.connect(":memory:")

def makebackuptofile(pdbfile):
    """
    makes a backup of the open database to a file
    :param pdbfile: backup to filesystem
    :return: connection of created backup
    """
    assert isopenDB(), "only backups of open database allowed"
    backupconn = sqlite3.connect(pdbfile)
    getdbcon().backup(backupconn)
    return backupconn

