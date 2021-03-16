from IM_DB import dbDML
from .baseobject import Baseobject
from .modelelement import Modelelemtype,Modelelement
from .externalref import Externalref
from .physicals import Storageformat


class Document(Baseobject):
    _tablename:str = 'documents'
    _prefix:str = 'docu'
    _columnlist:list = []

    def __init__(self,psrcname=None,psrcid=None):
        if (len(Document._columnlist) == 0): Document._columnlist = Baseobject.gettablecolumns(Document._tablename)
        super().__init__(tablename=self._tablename, prefix=self._prefix
                         ,pmodelemtype=Modelelemtype.DOCU
                         ,pscrid=psrcid
                         ,psrcname=psrcname
                         )

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Document._tablename
                               , psql="""
CREATE TABLE DOCUMENTS
    (
     DOCU_ID INTEGER NOT NULL primary key ,
     DOCU_NAME VARCHAR (60) NOT NULL ,
     DOCU_STFO_ID integer NULL ,
     DOCU_REFERENCE VARCHAR (500) NULL ,
     DOCU_CONTENT IMAGE NULL ,
     DOCU_DOCU_ID integer NULL
     ,CONSTRAINT DOCU_DOCU_FK FOREIGN KEY     (     DOCU_DOCU_ID)
		 REFERENCES DOCUMENTS     (     DOCU_ID )
	 ,CONSTRAINT DOCU_STFO_FK FOREIGN KEY (     DOCU_STFO_ID)
		 REFERENCES STORAGE_FORMATS (     STFO_ID )
	 
    )
"""
        )

    def getname(self,plang=None):
        return self.docu_name

    def getparent(self):
        return Document().getbyid(self.docu_docu_id)
    #getparent

    def getchildren(self):
        return Document.select(pwhere='docu_docu_id = {}'.format(self.docu_id)
                                              , porderby= 'docu_name')
    #getchildren

    def getformat(self):
        if self.docu_stfo_id is None: return None
        stfo = Storageformat().getbyid(pid=self.docu_stfo_id)
        return None if stfo is None else stfo.getname()

    @staticmethod
    def delete():
        Baseobject.delete(Document._tablename)

    @staticmethod
    def select(pwhere=None, porderby=None):
        return Baseobject.select(pclass=Document
                                 , pwhere=pwhere, porderby=porderby)
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
        """returns list of docu_ids references by an the element pid. (direct = TRUE) . For tables document reference via Interface is selected as well (direkt = FALSE)"""
        docus = dbDML.select("""
        select docu_id, direct
        from (select docu_id,docu_name,direct  
           from(
            select docu_id,docu_name 
                , MODO_MODE_ID as ref_id 
                ,'TRUE' direct
            from documents
            join mode_docu on MODO_docu_ID = docu_ID
            join modelelement on mode_id = MODO_MODE_ID
            join modelelem_type on melt_id = mode_melt_id
            union all 
            select docu_id, docu_name,tabl_id ref_id,'FALSE' direct
            from documents
            join mode_docu on MODO_docu_ID = docu_ID
            join (select intf_id,tabl_id
                  from tables
                  join interfaces on intf_ID = TABL_intf_ID
                 ) on MODO_MODE_ID = intf_ID      
            ) 
        where ref_id = {}  
        order by upper(docu_name)
        )
        """.format(pid))
        return docus

    def getrefmodes(self,pmelttype=None):
        return  Modelelement.select(
                pwhere="""mode_id in 
                            (select mode_id 
                            from mode_docu 
                            join modelelement on mode_id = modo_mode_id
                            where modo_docu_id = {}
                            and mode_type like '{}')"""
                    .format(self.docu_id,pmelttype if pmelttype is not None else '%')
              ,porderby="mode_id")

    @staticmethod
    def doculist():
        return Document.select(porderby='docu_name')
    #doculist

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
    _columnlist:list = []

    def __init__(self,pmodeid = None,pdocuid=None):
        if (len(ModelelemDocu._columnlist) == 0): ModelelemDocu._columnlist = Baseobject.gettablecolumns(ModelelemDocu._tablename)
        super().__init__(tablename=self._tablename, prefix=self._prefix)
        self.modo_mode_id = pmodeid
        self.modo_docu_id = pdocuid

    @staticmethod
    def delete(pwhere=None):
        Baseobject.delete(ModelelemDocu._tablename,pwhere=pwhere)

    @staticmethod
    def select(pwhere=None, porderby=None):
        return Baseobject.select(pclass=ModelelemDocu
                                 , pwhere=pwhere, porderby=porderby)
    @staticmethod
    def insertdocuref(pdocguidlist,pmodeid):
        if pdocguidlist is None: return
        for docguid in pdocguidlist:
            modo = ModelelemDocu()
            modo.modo_docu_id = Externalref.getODMmodeid(psrcid=docguid)
            modo.modo_mode_id = pmodeid
            modo.insert()
        #for
    #insertdocuref
#ModelelemDoku

