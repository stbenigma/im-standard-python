from IM_DB import dbDML
from SSOT_infra import logmessages
from .baseobject import Baseobject
from .modelelement import Modelelemtype,Modelelement
from .externalref import Externalref
from .physicals import Storageformat


class Document(Baseobject):
    _tablename:str = 'documents'
    _prefix:str = 'docu'
    _idcolname: str = _prefix + '_id'
    _modelemtype = Modelelemtype.DOCU
    _columnlist:list = []

    def __init__(self,psrcname=None,psrcid=None):

        super().__init__(pscrid=psrcid
                         ,psrcname=psrcname
                         )

    def getname(self,plang=None):
        return self.docu_name

    def getparent(self):
        return Document().getbyid(self.docu_docu_id)
    #getparent

    def getchildren(self):
        return Document.select(pwhere=('docu_docu_id = ?', self.docu_id), porderby='docu_name')
    #getchildren

    def getformat(self):
        if self.docu_stfo_id is None: return None
        stfo = Storageformat().getbyid(pid=self.docu_stfo_id)
        return None if stfo is None else stfo.getname()


    @staticmethod
    def updparent(pchildid,pparentid):
        if pchildid is not None and pparentid is not None:
            dbDML.exec("""
                update DOCUMENTS as DOK
                set docu_docu_ID = {}
                where docu_id = {}
                """.format(pparentid, pchildid))
        #if

    @staticmethod
    def updparentpairs(pparents):
        for val in pparents:
            # assume, exactly one child and one parent id
            childid, parentid = val[0], val[1]
            Document.updparent(pchildid=childid,pparentid=parentid)

    @staticmethod
    def updparents(psrcname,pparents):
        for key,val in pparents.items():
            # assume, exactly one child and one parent id
            childid = Externalref.getmodeid(psrcname=psrcname,psrcid=key)
            parentid = Externalref.getmodeid(psrcname=psrcname,psrcid=val)
            Document.updparent(pchildid=childid,pparentid=parentid)
    #updparents

    @staticmethod
    def getrefdoculist(pid):
        """returns list of docu_ids references by the element pid"""
        docus = dbDML.select("""
        select docu_id
        from (select docu_id,docu_name  
           from(
            select docu_id,docu_name 
                , MODO_MODE_ID as ref_id 
            from documents
            join mode_docu on MODO_docu_ID = docu_ID
            ) 
            where ref_id = {}  
            order by upper(docu_name)
        )
        """.format(pid))
        return docus

    def getrefmodes(self,pmelttype=None):
        return Modelelement.select(
            pwhere=("""mode_id in 
                            (select mode_id 
                            from mode_docu 
                            join modelelement on mode_id = modo_mode_id
                            where modo_docu_id = ?
                            and mode_type like ?)""",
                    self.docu_id, pmelttype if pmelttype is not None else '%'), porderby="mode_id")

    @classmethod
    def doculist(cls):
        return cls.select(porderby='docu_name')
    #doculist

    @classmethod
    def geticons(cls,pentiid):
        iconmasterdocumentname = "ENTITY-ICONS"
        """reads subdocuments of documents attached to an entity
        """
        return cls.select(pwhere=("""docu_id in (select modo_docu_id from mode_docu 
                                                    where modo_mode_id = ?)
                                    and docu_docu_id in (select docu_id from documents 
                                                        where docu_name = ?)""",pentiid,iconmasterdocumentname))

    """def xxdocureferenced(prelaid=None,penti=None,pwebattr=None):
    data = dbDML.select("
    select child.docu_id, child.docu_NAME,child.docu_stfo_id,child.docu_REFERENZ
       ,parent.docu_ID parent_id,parent.docu_NAME parent_name
 from  docuMENTE child
left join dokumente parent on parent.docu_ID = child.docu_docu_ID  
join MODELELEM_docu on MODO_docu_ID = child.docu_ID
join modellelement on mode_id = MODO_MODE_ID
where  (   mode_rela_id = {}
        or mode_enti_id = {}
        or mode_attr_id = {}
       ) ".format (prelaid,penti,pwebattr))
    return data
#docureferenced
"""
#Document

class ModelelemDocu(Baseobject):
    _tablename:str = 'mode_docu'
    _prefix:str = 'modo'
    _idcolname: str = _prefix + '_id'
    _columnlist:list = []

    def __init__(self,pmodeid = None,pdocuid=None):

        super().__init__()
        self.modo_mode_id = pmodeid
        self.modo_docu_id = pdocuid


    @staticmethod
    def insertdocuref(pdocguidlist,pmodeid):
        if pdocguidlist is None: return
        for docguid in pdocguidlist:
            modo = ModelelemDocu()
            modo.modo_docu_id = Externalref.getODMmodeid(psrcid=docguid)
            if modo.modo_docu_id is None:
                #GUID no longer exists
                logmessages.writelog("Document ({}) referenced in model-element id={} does not exist".format(docguid, pmodeid))
                return
            modo.modo_mode_id = pmodeid
            modo.insert()
        #for
    #insertdocuref
#ModelelemDoku

