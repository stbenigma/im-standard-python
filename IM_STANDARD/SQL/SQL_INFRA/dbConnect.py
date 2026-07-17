import logging
import sqlite3

def dbval(val):
    """translates None into NULL,
                str(int) if integer
                string into 'string'
                boolean into 'TRUE'/'FALSE'
                """
    return 'NULL' if val is None \
        else ('TRUE' if val else "FALSE") if isinstance(val, bool) \
        else str(val) if isinstance(val,int) or isinstance(val,float) \
        else val


def dict_factory(cursor, row):
    """
    return rows as dict's (instead of default lists)
    passed as a dynamic function to select
    :param cursor:
    :param row:
    :return:
    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class SqliteDb:
    class DBError(Exception):
        """Base for all DB errors"""
        def __init__(self, msg, original: Exception = None):
            super().__init__(msg)
            self.original = original

    class NO_DATA_FOUND(sqlite3.IntegrityError):
        """Raised when a query returns no rows."""
        def __init__(self, *args, **kwargs):  # real signature unknown
            pass

    class TOO_MANY_ROWS(sqlite3.IntegrityError):
        """Raised when a query returns more rows than expected."""
        def __init__(self, *args, **kwargs):  # real signature unknown
            pass

    class UK_VIOLATED(sqlite3.IntegrityError):
        """Raised when in an update or insert an uk constraint is violated"""
        def __init__(self, *args, **kwargs):  # real signature unknown
            pass

    class FK_VIOLATED(sqlite3.IntegrityError):
        """Raised when in an update or insert an fk constraint is violated"""
        def __init__(self, *args, **kwargs):  # real signature unknown
            pass

    class CHECK_VIOLATED(sqlite3.IntegrityError):
        """Raised when in an update or insert an fk constraint is violated"""
        def __init__(self, *args, **kwargs):  # real signature unknown
            pass

    class NOTNULL(sqlite3.IntegrityError):
        """Raised when in an update or insert an fk constraint is violated"""
        def __init__(self, *args, **kwargs):  # real signature unknown
            pass

    def raise_integrity_error(e: sqlite3.IntegrityError):
        name = getattr(e, "sqlite_errorname", "") or ""
        if name == "SQLITE_CONSTRAINT_FOREIGNKEY":
            raise SqliteDb.FK_VIOLATED(str(e), e) from e
        elif name == "SQLITE_CONSTRAINT_UNIQUE":
            raise SqliteDb.UK_VIOLATED(str(e), e) from e
        elif name == "SQLITE_CONSTRAINT_CHECK":
            raise SqliteDb.CHECK_VIOLATED(str(e), e) from e
        elif name == "SQLITE_CONSTRAINT_NOTNULL":
            raise SqliteDb.NOTNULL(str(e), e) from e
        else:
            raise SqliteDb.DBError(str(e), e) from e

    SQLITE_SETUP = ["PRAGMA foreign_keys = ON;",
                    "PRAGMA synchronous = OFF;",
                    "PRAGMA journal_mode = OFF;",
                    "PRAGMA temp_store = MEMORY;"
                    ]
    def __init__(self, filepath=None):
        """
        creates an empty sqlite inmemory database accessible as "connection"
        if filepath is given, reads a database and copies it into the inmemory database
        if filepath is not given, the new database is empty
        @param filepath: filepath to a sqlite databasefile
        """
        self._myconnection: sqlite3.Connection = self._connectmemorydb()
        self._makedbsafe()
        if filepath is not None:
            #read filedatabase into memory and remember
            self._readdbfromfile(filepath=filepath)
        self._filepath = filepath # remember my fileorigin (if there was any)
        return

    @staticmethod
    def _connectmemorydb() -> sqlite3.Connection:
        return sqlite3.connect(":memory:")

    @property
    def connection(self) -> sqlite3.Connection:
        return self._myconnection

    def dbisempty(self):
        """
        :return: True if database contains only system tables.
        """
        cursor = self.connection.cursor()
        # get all tablenames except system tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = cursor.fetchall()

        return len(tables) == 0

    def writedbtofile(self, filepath:None):
        """
        makes a backup of the open database to a file
        :param filepath: filenpath to write the database to

        """
        locfilepath=filepath if filepath is not None else self._filepath
        assert locfilepath is not None,"No filepath given to write db to."
        backupconn = sqlite3.connect(filepath)
        self.connection.backup(backupconn)
        return

    def _makedbsafe(self):
        """
        applies the startup sql for a save database
        :return:
        """
        cursor = self.connection.cursor()
        try:
            cursor.executescript("\n".join(self.SQLITE_SETUP))
            self.connection.commit()
        except sqlite3.Error as e:
            logging.error(f"Error while executing  startupscript: {e}")
        return

    def _readdbfromfile(self, filepath):
        """
        reads a sqlite database from a file and stores it in a memory database
        fails if database contains already tables
        :param: filepath of sqlite database

        :return:
        """
        assert self.dbisempty(), f"current inmemory db is not empty"
        try:
            locconn = sqlite3.connect(filepath)
        except sqlite3.Error as e:
            # if re.match("table .* already exists", e.__str__()):
            #    pass
            # else:
            logging.error(f"Unexpected SQL-error: \t{e}")
            raise e
        # make a copy = "backup" into my memory database
        locconn.backup(self.connection)
        locconn.close()

        self._makedbsafe()
        return

    """ 
    possible function to extend the sqliteDB class
    PRAGMA page_count;: Gibt die Gesamtanzahl der Seiten in der Datenbank zurück.
        PRAGMA page_size;: Gibt die Größe einer einzelnen Seite in Bytes zurück.
            Berechnung: page_count * page_size /1024/1024 = Gesamtgröße im RAM.

    PRAGMA table_info(<table_name>);:
     Listet alle Spalten einer Tabelle inklusive Datentyp, Primary Key und Default-Werten auf.

    PRAGMA foreign_key_list(<table_name>);: 
    Zeigt alle Fremdschlüsselbeziehungen der angegebenen Tabelle an.

    PRAGMA index_list(<table_name>);: 
    Gibt alle Indizes zurück, die für eine Tabelle erstellt wurden.
    """

