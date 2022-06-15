import os
import re
import sqlite3
import logging
from datetime import datetime

from SSOT_db.SQL_INFRA import dbDDL, dbDML
from SSOT_infra import logmessages, nvl
from datetime import datetime

# custom logging levels below logging.DEBUG
FAILED_SQL = 6
SUCCESSFUL_SQL = 5

logger = logging.getLogger('baseobject')

sqltrace = logging.getLogger('sqltrace')
sqltrace.setLevel(SUCCESSFUL_SQL)  # trace level

stamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
sql_trace_handler = logging.FileHandler(f'sqlite-{stamp}.log')
sqltrace.addHandler(sql_trace_handler)


def prettyprint(v):
    if type(v) in (int, float):
        return v
    elif type(v) is str:
        return f"'{v[0:40]}{'...' if len(v) > 40 else ''}'"
    else:
        return f"'{v}'"


class Boolean:
    TRUE: str = 'TRUE'
    FALSE: str = 'FALSE'

    @classmethod
    def str2bool(cls, pstr):
        if (pstr is None):
            return None
        elif (pstr.upper() in (cls.TRUE, 'T')):
            return True
        elif (pstr.upper() in (cls.FALSE, 'F')):
            return False
        else:
            raise Exception('Ungültiger Wert für Boolean "{}"'.format(pstr))

    @classmethod
    def bool2str(cls, bool):
        return cls.TRUE if bool else cls.FALSE

    @classmethod
    def strnegbool(cls, pstr):
        return cls.bool2str(not cls.str2bool(pstr))


# Boolean


class UniqueKeyException(Exception):
    pass


class ForeignKeyException(Exception):
    pass


class Baseobject:
    _modelemtype = None  # if not overwritten, the object is no Modelelement

    defaultCreator: str = "sys"

    def fullcolname(self, col):
        return self._prefix + '_' + col

    def colvalue(self, pcolname):
        try:
            return self.__getattribute__(pcolname.lower())
        except:
            return None

    def setcolvalue(self, pcolname, pvalue):
        self.__setattr__(pcolname.lower(), pvalue)

    def setdefaultval(self, pcolname, pvalue):
        col = self.fullcolname(pcolname.lower())
        if col in self._columnlist.keys():
            if self.colvalue(col) is None: self.setcolvalue(col, pvalue)

    def __init__(self, **kwargs):
        if (len(self.__class__._columnlist) == 0): self.__class__._columnlist = Baseobject.gettablecolumns(
            self._tablename)
        self.__emptyclass()

        self.__srcname = kwargs['srcname'] if ('srcname' in kwargs) else kwargs['psrcname'] if (
                'psrcname' in kwargs) else None
        # old spelling
        self.__srcid = kwargs['srcid'] if ('srcid' in kwargs) else kwargs['psrcid'] if ('psrcid' in kwargs) \
            else kwargs['pscrid'] if ('pscrid' in kwargs) else None
        for col, val in kwargs.items():
            if col in self.__class__._columnlist:
                self.setcolvalue(col, Boolean.bool2str(val) if type(val) == bool else val)
            else:
                assert col in (
                    "srcid", "srcname", "psrcid", "pscrid",
                    "psrcname"), f"parameter ({col}) not allowed for {type(self)}"
        self.setdefaultvalues()

        return

    def __emptyclass(self):
        for col in self._columnlist.keys():
            self.setcolvalue(pcolname=col, pvalue=None)

    # emptyclass

    def _semanticcols(self):
        """Return list of columns without standard management columns"""
        return list(
            set(self._columnlist.keys()).difference((self.fullcolname(n) for n in ['id', 'uc', 'um', 'dc', 'dm'])))

    def semanticequal(self, pbrother, pequalexceptlist=[]):
        """ true, if all semantic elements are equal. Managing attributes (id, uc,dc etc.) are excluded"""
        for sc in self._semanticcols():
            if (sc not in pequalexceptlist) and (nvl(self.colvalue(sc)) != nvl(pbrother.colvalue(sc))):
                return False
        return True

    def semanticcopy(self, pbrother):
        """ copies  all semantic elements. Managing attributes (id, uc,dc etc.) are excluded"""
        for sc in self._semanticcols():
            self.setcolvalue(pcolname=sc, pvalue=pbrother.colvalue(sc))

    def getname(self, plang=None):
        """if object has name, it must be overwritten"""
        return "{} ({}) has no name".format(self._prefix, self.getid())

    def toarray(self):
        return [self.__dict__[col] for col in self._columnlist.keys()]

    def totuple(self):
        return tuple(self.toarray())

    @classmethod
    def to_sql_values(cls, values: []) -> [str]:
        result = []
        for value in values:
            if value is None:
                result.append('null')
            elif isinstance(value, str):
                result.append(f"'{value}'")
            elif isinstance(value, datetime):
                result.append(f"'{value}'")
            else:
                result.append(str(value))
        return result

    def _fromarray(self, parr):
        for cnt, val in enumerate(parr):
            collist = {colvalue[0]: colname for colname, colvalue in self._columnlist.items()}
            self.__dict__[collist[cnt]] = val
        return self

    def getid(self):
        return self.colvalue(self._idcolname)

    def getidcolname(self):
        return self._idcolname

    def setid(self, pid):
        self.setcolvalue(pcolname=self._idcolname, pvalue=pid)

    def getsrcname(self):
        return self.__srcname

    def getsrcid(self):
        return self.__srcid

    def insert(self, pdoerrhdlng=True):
        self.setdefaultval(pcolname='dc', pvalue=datetime.today())
        self.setdefaultval(pcolname='uc', pvalue=Baseobject.defaultCreator)
        """wird erst bei  update gemacht        
        if self.colvalue(self.fullcolname('dm')) is None: self.setcolvalue(self.colvalue(self.fullcolname('dm')), datetime.today())
        if self.colvalue(self.fullcolname('um')) is None: self.setcolvalue(self.colvalue(self.fullcolname('um')), Baseobject.defaultCreator)
        """
        if self._modelemtype is not None:
            try:
                locid = Modelelement(pid=self.getid(), pmeltshortname=self._modelemtype).insert()
                self.setid(locid)
            except UniqueKeyException as e:
                assert e
                locid = self.getid()
                logger.debug(f"Modelelement for {self.getid()} already exists")

        lsql = """insert into {} ({}) values ({})
           """.format(self._tablename, self.columnsliststring()
                      , self.columnsliststring(pplaceholder=True))
        try:
            id = dbDML.insert(lsql, self.totuple())
            if self.getid() is None:
                self.setid(id)  # autocolumns zurücklesen
            logger.debug(f"Created new entry (id:{id}) in {self._tablename} from " \
                         f"{Baseobject.print_sql_placeholder_values(lsql, self.totuple())}")
            self.trace(SUCCESSFUL_SQL, lsql, self.toarray())
        except sqlite3.Error as e:
            msg = f"Cannot insert into {self._tablename} tuple {self.totuple()}." \
                  f"\n{e} from statement \n{Baseobject.print_sql_placeholder_values(lsql, self.totuple())}"

            if pdoerrhdlng:
                try:
                    logmessages.writelog(str(e))
                    logmessages.writelog(self.tostring())
                    if self._modelemtype is not None:
                        Modelelement.delete(pwhere=("mode_id = ?", locid))
                except:
                    print("Loggin-Error in Baseobject.insert():")
                    print(str(e))
                    print(lsql)
                    print(self.totuple())

                self.trace(FAILED_SQL, lsql, self.toarray(), e)

            # if
            if str(e).startswith("UNIQUE constraint failed"):
                raise UniqueKeyException(msg) from e
            elif str(e).startswith("FOREIGN KEY constraint failed"):
                raise ForeignKeyException(msg) from e
            else:
                raise Exception(msg) from e

        # try
        if self.__srcname is not None:
            try:
                Externalref(extr_source_name=self.__srcname, extr_source_id=self.__srcid,
                            extr_mode_id=self.getid()).insert(
                    pdoerrhdlng=pdoerrhdlng)

            except Exception as e2:
                # delete original entry
                self.delete(pwhere=(f"{self._idcolname} = ?", locid))
                raise Exception() from e2

        return self.getid()

    def updatedb(self, pdoerrhdlng=True):
        now = datetime.today()
        self.setdefaultval(pcolname='dm', pvalue=now)
        self.setdefaultval(pcolname='um', pvalue=Baseobject.defaultCreator)

        updcollist = list(self._columnlist.keys())
        updcollist.remove(self._idcolname)  # ID will never be changed, it is the where-condition
        lsql = f"""update {self._tablename} """
        lsql += """\nset {}""".format('\n,'.join(col + " = ?" for col in updcollist))
        lsql += f"""\nwhere {self._idcolname} = {dbDML.dbval(self.getid())}"""
        values = [self.colvalue(pcolname=col) for col in updcollist]
        # print (lsql)
        try:
            id = dbDML.exec(lsql, *values)
            self.trace(SUCCESSFUL_SQL, f"update {self._tablename} {self.update_set_statement(updcollist)}"
                                       f" where {self._idcolname} = {dbDML.dbval(self.getid())}"
                       , values)
        except sqlite3.Error as e:
            if pdoerrhdlng:
                try:
                    logmessages.writelog(str(e))
                    logmessages.writelog(self.tostring())
                except:
                    print("Loggin-Error in Baseobject.updatedb():")
                    print(str(e))
                    print(lsql)
                    print(self.totuple())
            # if
            self.trace(FAILED_SQL, f"update {self._tablename} set {self.update_set_statement(updcollist)}"
                                   f" where {self._idcolname} = {dbDML.dbval(self.getid())}",
                       values, e)
            raise e
        # try
        if self.__srcname is not None:
            Externalref.setlastupdate(psrcname=self.__srcname,
                                      psrcid=self.__srcid,
                                      pmodeid=self.getid())
        return

    def update_set_statement(self, columns: []):
        values = [f"{t[0]} = {t[1]}" for t in
                  zip(columns, self.to_sql_values([self.colvalue(pcolname=col) for col in columns]))]
        return ', '.join(values)

    def gettablecolumns(ptablename):
        sql = "PRAGMA table_info({})".format(ptablename)
        try:
            cols = dbDML.select(sql)
            defval = lambda val: None if val is None else val.strip("'").strip('"')
            retval = {c[1].lower(): [c[0], defval(c[4])] for c in cols}
        except:
            retval = {}
        return retval

    def setdefaultvalues(self):
        for colname, colvalue in self._columnlist.items():
            if self.colvalue(colname) is None:
                self.setcolvalue(pcolname=colname, pvalue=colvalue[1])
        return

    def tostring(self):
        lretval = "Table: {}\n".format(self._tablename)
        lretval += "\n".join("{} = '{}'".format(col, self.colvalue(col)) for col in self._columnlist.keys())
        return lretval

    def getbyid(self, pid):
        if pid is None: return None
        data = self.select(pwhere=(f"{self._idcolname}=?", pid))
        if (len(data) > 1):
            logmessages.writelog(f"{self._tablename}: nonunique ID={pid}'")
            raise Exception(f'{self._tablename}: nonunique ID={pid}')
        elif (len(data) == 0):
            logmessages.writelog(f"{self._tablename}: nonexistent ID={pid} '")
            raise Exception(f'{self._tablename}: nonexistent ID={pid}')
        else:
            self = data[0]
        return self

    # getbyid

    def trace(self, level, statement, values: list, exception: Exception = None):
        try:
            sql_statement = statement
            if 'insert' in statement.lower():
                str_values = self.to_sql_values(values)
                value_string = 'values (' + ', '.join(str_values) + ')'
                sql_statement = re.sub(r"values \(.+\).*", value_string, statement).rstrip()

            if 'update' in statement.lower():
                sql_statement = re.sub(r'\s+', r' ', statement.replace('\n', ' '), re.MULTILINE | re.DOTALL)
                if exception is not None:
                    exception = exception.args[-1]

            if exception is not None:
                args = ''
                if isinstance(exception, BaseException):
                    args = f"{os.linesep}{os.linesep.join(exception.args)}"
                sql_statement = f"! {sql_statement}\n {exception.__class__}: {str(exception)}{args}"
            sqltrace.log(level, sql_statement)
        except Exception as e:
            logger.error(f"Cannot log error {statement}", exc_info=e)

    @classmethod
    def getbyuk(cls, **colvalpairs):
        """{colname:colvalue,}"""
        wherecond = dbDML.valuepairs2sqlexpr(**colvalpairs)
        data = cls.select(pwhere=wherecond)
        if (len(data) > 1):
            raise Exception('{}: nonunique {}'.format(cls._tablename, wherecond))
        elif (len(data) == 0):
            retval = None
        else:
            retval = data[0]
        # fi
        return retval

    def getbyanyuk(self):
        """return a new object selected with the uk-values of self.
            if there is no uk return None
            if there are several uk's
                try each one
                if a uk-select returns more than 1 row
                    error too many rows
                if the number of different rows returned from all uk's lookup
                    = 0 return None
                    = 1 return this row
                    > raise error (different rows found)
                    """
        uklist = dbDDL.getuklist(ptablename=self._tablename)
        if len(uklist) == 0: return None
        foundrows = []
        """uklist = [[colname,],]"""
        for uk in uklist:
            row = self.getbyuk(**{colname: self.colvalue(colname) for colname in uk})
            if row is not None: foundrows.append(row)
        # for
        # make a list of  all id's of the found elements
        idset = set([r.getid() for r in foundrows])
        if len(idset) == 0: return None
        if len(idset) == 1: return foundrows[0]
        raise Exception(
            "ID set {} -> rows '{}' found for different uk's of table {}, id={}".format(idset,
                                                                                        ', '.join(
                                                                                            [str(a.totuple()) for a in
                                                                                             foundrows]),
                                                                                        self._tablename, self.getid()))
        return

    def prefix(self):
        return self._prefix

    def _getmode(self):
        if self._modelemtype is None: return None
        mode = Modelelement().getbyid(self.getid())
        return mode

    def getminzoomlevel(self):
        mode = self._getmode()
        return None if mode is None else mode.mode_min_zoom_level

    def getmaxzoomlevel(self):
        mode = self._getmode()
        return None if mode is None else mode.mode_max_zoom_level

    def getpublstatus(self):
        mode = self._getmode()
        return None if mode is None else mode.mode_publ_status

    def getbyextref(self, psrcid, psrcname):
        if self._modelemtype is None: return None
        mode = Modelelement.getmodebyextref(psrcname=psrcname, psrcid=psrcid)
        if mode is None or mode.mode_type != self._modelemtype: return None
        return self.getbyid(mode.mode_id)

    def getIDbyextref(self, psrcid, psrcname):
        ref = self.getbyextref(psrcid=psrcid, psrcname=psrcname)
        return None if ref is None else ref.getid()

    def getukvaluepairs(self):
        uklist = dbDDL.getuklist(ptablename=self._tablename)
        return [dbDML.valuepairs2sqlexpr(**{colname: self.colvalue(colname) for colname in uk}) for uk in uklist]

    def getfkcolumns(self):
        """{colname: (fktable, fkcolname,fkprefix)} all names in lowercase"""
        fkcols = dbDDL.getfklist(ptablename=self._tablename)
        retval = {}
        for col, fk in fkcols.items():
            fk.append(fk[1][0:4])
            retval[col] = fk
        return retval

    def getelementdescs(self):
        from SSOT_db.IM_OBJECTS import table2class

        fks = self.getfkcolumns()

        def getparentdesc(colname):
            val = self.colvalue(colname)
            if colname in fks:
                tablename = fks[colname][0]
                if tablename in table2class:
                    return f"{colname}=>{table2class[tablename]().getbyid(val).descrstr()}"
                else:
                    return f"{tablename}: {colname}={prettyprint(val)}"
            else:
                return f"{colname}={prettyprint(val)}"

        retval = []
        uklist = dbDDL.getuklist(ptablename=self._tablename)
        for uk in uklist:
            retval.append(', '.join(getparentdesc(col) for col in uk))
        return retval

    def __str__(self):
        retval = f"{self._tablename.capitalize()}: "
        retval += ', '.join(f"{col}={prettyprint(self.colvalue(col))}" for col in self._columnlist)
        return retval

    def descrstr(self):
        descrs = self.getelementdescs()
        if len(descrs) == 0:
            retval = self.__str__()
        else:
            retval = f"{self._tablename.capitalize()}: "
            retval += descrs[0]
        return retval

    @classmethod
    def defaultorderby(cls):
        return cls.__dict__.get('_defaultorderby')

    @classmethod
    def select(cls, pwhere=None, porderby=None):
        if (len(cls._columnlist) == 0): cls._columnlist = Baseobject.gettablecolumns(cls._tablename)
        if porderby is None:
            porderby = cls.defaultorderby()
        lsql = f"""select {cls.columnsliststring()} 
                        from {cls._tablename} as {cls._prefix} 
                        {"" if pwhere is None else f"where {pwhere if type(pwhere) is str else pwhere[0]}"} 
                        {"" if porderby is None else f"order by {porderby}"} """
        arguments = ()
        if type(pwhere) is tuple and len(pwhere) > 1:
            arguments = (*arguments, *pwhere[1:])

        data = dbDML.select(lsql, *arguments)
        retval = []
        for d in data:
            obj = cls()._fromarray(d)
            try:
                """obj ist vom Typ des Subtypes"""
                """ist in MultilangBaseobject definiert"""
                obj.getsprachvals()
            except AttributeError as err:
                pass
            except Exception as err:
                raise err
            retval.append(obj)
        return retval

    # select

    @classmethod
    def delete(cls, pwhere=None):
        arguments = ()
        if type(pwhere) is tuple and len(pwhere) > 1:
            arguments = (*arguments, *pwhere[1:])

        wherecond = lambda arg: "" if arg is None else " where {}".format(arg if type(arg) is str else arg[0])
        try:
            modedelcnt = 0
            if cls._modelemtype is not None:
                statement = "select {} from {}".format(cls._idcolname, cls._tablename)
                if pwhere is not None:
                    statement += wherecond(pwhere)
                modedelcnt = Modelelement.delete(pwhere=("mode_id in ({})".format(statement), *arguments))
            # fi
            statement = """delete from {} {}""" \
                .format(cls._tablename, wherecond(pwhere))
            elemdelcnt = dbDML.delete(statement, *arguments)
            retval = elemdelcnt + modedelcnt  # cascade delete from MODE has to be counted as well
        except Exception as err:
            message = f"Cannot delete element {statement}\nArguments: {str(arguments)}"
            if cls._tablename in ['examples', 'synonyms']:
                logger.warning(f"Ignoring fk error on delete {cls._tablename}:\n{message}")
                retval = 0
            else:
                raise Exception(message) from err

        return retval

    @classmethod
    def deletemissingids(cls, pids: tuple):
        cnt = 0
        if len(pids) > 0:
            cnt = cls.delete(pwhere=(f"{cls._idcolname} not in ({','.join('?' * len(pids))})", *pids))
        return cnt

    @classmethod
    def columnsliststring(cls, pplaceholder=False):
        return ','.join('?' if pplaceholder else col for col in cls._columnlist.keys())

    @classmethod
    def print_sql_placeholder_values(cls, sql: str, values: tuple):
        result = sql
        pattern = re.compile(r"[^(]+\(([^)]+)\)[^(]*(\([^)]*\))?.*")
        matcher = pattern.match(sql)
        if matcher is not None:
            columns = matcher.group(1).split(',')
            vit = iter(values)
            bracket_content = []
            for column in columns:
                bracket_content.append(column + '=' + str(next(vit)))
            result = result.replace(matcher.group(1), ', '.join(bracket_content))
            if len(matcher.group(2)) > 0:
                result = result.replace(matcher.group(2), '(...)')
        return result


# Baseobject

class MultilangBaseobject(Baseobject):
    def __init__(self, multilangcols, **kwargs):
        super().__init__(**kwargs)
        self._multilangcols = multilangcols
        return

    def getmodeid(self):
        raise NotImplementedError("'getmodeid' muss implementiert werden")

    def getsprachvals(self):
        for col in self._multilangcols:
            spt = Languagetext.getlang_texts(pattrname=self._multilangcols[col], pmodeid=self.getid())
            self.setcolvalue(pcolname=col + '_l', pvalue=spt)
        # for
        return

    def _getsprachval(self, colname, plang=None):
        try:
            retval = self.colvalue(colname + '_l')[plang]
        except:
            # keine sprache oder keinen Namen für Language
            retval = self.colvalue(colname)
        # try

        return retval


from .languagetext import Languagetext
from .modelelement import Modelelement
from .externalref import Externalref
