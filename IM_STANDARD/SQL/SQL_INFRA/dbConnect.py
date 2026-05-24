import logging
import sqlite3

def dbval(val):
    """translates None into NULL,
    str(int) if integer
    string into 'string'
    boolean into TRUE/FALSE
    """
    return 'NULL' if val is None \
        else ('TRUE' if val else "FALSE") if isinstance(val, bool) \
        else str(val) if isinstance(val,int) or isinstance(val,float) \
        else val



def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class SqliteDb:
    SQLITE_SETUP = ["PRAGMA foreign_keys = ON;",
                    "PRAGMA synchronous = OFF;",
                    "PRAGMA journal_mode = OFF;",
                    "PRAGMA temp_store = MEMORY;"
                    ]
    """ PRAGMA page_count;: Gibt die Gesamtanzahl der Seiten in der Datenbank zurück.
        PRAGMA page_size;: Gibt die Größe einer einzelnen Seite in Bytes zurück.
            Berechnung: page_count * page_size /1024/1024 = Gesamtgröße im RAM.
    """
    """
    creates an empty sqlite inmemory database accessible as "connection"
    if filepath is given, reads a database and copies it into the inmemory database
    if filepath is not given, the new database is empty
    """
    """PRAGMA table_info(<table_name>);:
     Listet alle Spalten einer Tabelle inklusive Datentyp, Primary Key und Default-Werten auf.

    PRAGMA foreign_key_list(<table_name>);: 
    Zeigt alle Fremdschlüsselbeziehungen der angegebenen Tabelle an.

    PRAGMA index_list(<table_name>);: 
    Gibt alle Indizes zurück, die für eine Tabelle erstellt wurden.
    """

    def __init__(self, filepath=None):
        self._myconnection: sqlite3.Connection = self._connectmemorydb()
        self._makedbsafe()
        self._filepath = None
        if filepath is not None:
            self._readdbfromfile(filepath=filepath)
        return

    @staticmethod
    def _connectmemorydb() -> sqlite3.Connection:
        return sqlite3.connect(":memory:")

    @property
    def connection(self) -> sqlite3.Connection:
        return self._myconnection

    def dbisempty(self):
        cursor = self.connection.cursor()
        # get all tablenames except system tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = cursor.fetchall()

        return len(tables) == 0

    def writedbtofile(self, filepath):
        """
        makes a backup of the open database to a file
        :param filepath: filenpath to write the database to

        """
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
            # remember, where I came from
            self._filepath = filepath
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
