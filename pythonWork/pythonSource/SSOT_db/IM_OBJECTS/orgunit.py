from SSOT_db.SQL_INFRA import dbDML
from SSOT_infra import logmessages
from .baseobject import Baseobject
from .modelelement import Modelelemtype,Modelelement
from .externalref import Externalref


class OragnisationalUnit(Baseobject):
    _tablename:str = 'organisationalunits'
    _prefix:str = 'orgu'
    _idcolname: str = _prefix + '_id'
    _modelemtype = Modelelemtype.ORGU
    _columnlist:list = []

    def __init__(self,psrcname=None,psrcid=None):

        super().__init__(pscrid=psrcid
                         ,psrcname=psrcname
                         )

    def getname(self,plang=None):
        return self.orgu_name

    def getparent(self):
        return Document().getbyid(self.orgu_orgu_id)
    #getparent

    def getchildren(self):
        return Document.select(pwhere=('orgu_orgu_id = ?', self.orgu_id), porderby='orgu_name')
    #getchildren

    @staticmethod
    def updparent(pchildid, pparentid):
        if pchildid is not None and pparentid is not None:
           dbDML.exec("""
            update organisationalunits as ou_C
            set orgu_orgu_ID = {}
            where orgu_id = {}
            """.format(pparentid, pchildid))

    @staticmethod
    def updparentpairs(pparents):
        """pparentpairs = [(orgu_id, parent_id),]"""
        for val in pparents:
            # assume, exactly one child and one parent id
            childid,parentid = val[0],val[1]
            OragnisationalUnit.updparent(pchildid=childid,pparentid=parentid)
    #updparents

    @staticmethod
    def updparents(psrcname,pparents):
        """pparents = [(orgu_id, parent_id),]"""
        for key,val in pparents.items():
            # assume, exactly one child and one parent id
            childid = Externalref.getmodeid(psrcname=psrcname,psrcid=key)
            parentid = Externalref.getmodeid(psrcname=psrcname,psrcid=val)
            OragnisationalUnit.updparent(pchildid=childid,pparentid=parentid)
    #updparents

    def getrefmodes(self,pmelttype=None):
        return  Modelelement.select(
                pwhere=("""mode_id in 
                            (select mode_id 
                            from mode_orgu 
                            join modelelement on mode_id = moou_mode_id
                            where moou_orgu_id = ?
                            and mode_type like ?)""",
                    self.orgu_id, pmelttype if pmelttype is not None else '%'))

    @staticmethod
    def getreforgulist(pid):
        """returns list of orgu_ids references by an the element pid. """
        orgus = dbDML.select("""
         select orgu_id
         from (select orgu_id,orgu_name  
            from(
             select orgu_id,orgu_name ,
                 MOOU_MODE_ID as ref_id 
             from organisationalunits
             join mode_orgu on MOOU_orgu_ID = orgu_ID
             ) 
         where ref_id = {}  
         order by upper(orgu_name)
         )
         """.format(pid))
        return orgus

    @staticmethod
    def orgulist():
        return OrganisationalUnit.select(porderby='orgu_name')
    #orgulist
#OragniastionalUnit

class ModelelemOrgu(Baseobject):
    _tablename:str = 'mode_orgu'
    _prefix:str = 'moou'
    _idcolname: str = _prefix + '_id'
    _columnlist:list = []

    def __init__(self,pmodeid=None,porguid = None):

        super().__init__()
        self.moou_mode_id = pmodeid
        self.moou_orgu_id = porguid


    @staticmethod
    def insertorguref(porguidlist, pmodeid):
        if porguidlist is None: return
        for orguguid in porguidlist:
            moou = ModelelemOrgu()
            moou.moou_orgu_id = Externalref.getODMmodeid(psrcid=orguguid)
            if moou.moou_orgu_id is None:
                #GUID no longer exists
                logmessages.writelog("Org-Unit ({}) referenced in model-element id={} does not exist".format(orguguid, pmodeid))
                return
            moou.moou_mode_id = pmodeid
            moou.insert()
        #for
    #insertdocuref
#ModelelemDoku

