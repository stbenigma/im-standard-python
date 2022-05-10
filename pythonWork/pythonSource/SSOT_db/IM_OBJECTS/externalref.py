from .baseobject import Baseobject
from SSOT_db.SQL_INFRA import dbDML
from datetime import datetime


class Externalref(Baseobject):
    _tablename: str = 'external_refs'
    _prefix: str = 'extr'
    _idcolname: str = _prefix + '_id'
    _columnlist = dict()
    _defaultorderby = "extr_id"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.extr_last_update = self.extr_last_update or datetime.today()

    @staticmethod
    def setlastupdate(psrcname, pmodeid, psrcid=None):
        extr: Externalref = Externalref().getbyuk(extr_source_name=psrcname, extr_mode_id=pmodeid)
        if extr is None:
            """not found, insert it"""
            Externalref(extr_source_name=psrcname,
                        extr_mode_id=pmodeid,
                        extr_source_id=psrcid,
                        extr_last_update=datetime.today()).insert()
        else:
            extr.extr_last_update = datetime.today()
            if psrcid is not None: extr.extr_source_id = psrcid
            extr.updatedb()
        return

    @staticmethod
    def getsources():
        data = dbDML.select("""select distinct extr_source_name from external_refs order by extr_source_name""")
        return [d[0] for d in data]

    @staticmethod
    def getsrcinfo(pmodeid):
        extrs = Externalref.select(pwhere=("extr_mode_id = ?", pmodeid)
                                   , porderby="extr_source_name,extr_source_id")
        list = {e.extr_source_name: [e.extr_source_id, e.extr_last_update] for e in extrs}
        return list

    # getsrcsinfo

    @staticmethod
    def getextr(psrcname, pmodeid=None, psrcid=None):
        extr = Externalref.select(pwhere=("extr_source_name = ? and {}".format(
            "extr_mode_id = ?" if pmodeid is not None else "extr_source_id = ?"
        ), psrcname, pmodeid if pmodeid is not None else psrcid)
        )
        return extr

    @staticmethod
    def getsrcid(psrcname, pmodeid):
        extrs = Externalref.getextr(psrcname=psrcname, pmodeid=pmodeid)
        srcid = None if len(extrs) == 0 else extrs[0].extr_source_id
        return srcid

    @staticmethod
    def getallextrs(pelemtype,psrcname=None):
        return Externalref.select(pwhere=("""extr_mode_id in (select mode_id 
                                                        from modelelement 
                                                        where upper(mode_type) = upper(?)
                                             and extr_source_name like ?)""",
                                          pelemtype,'%' if psrcname is None else psrcname))

    @staticmethod
    def getmodeid(psrcname, psrcid):
        extrs = Externalref.getextr(psrcname=psrcname, psrcid=psrcid)
        modeid = None if len(extrs) == 0 else extrs[0].extr_mode_id
        return modeid

    @staticmethod
    def existssrcid(psrcname, psrcid):
        extrs = Externalref.getextr(psrcname=psrcname, psrcid=psrcid)
        return (len(extrs) > 0)

# Externalref
