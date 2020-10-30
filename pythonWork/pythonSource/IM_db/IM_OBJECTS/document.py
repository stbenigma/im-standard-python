from IM_DB import dbDML
from .baseobject import Baseobject
from .modelelement import Modelelemtype
from .externalref import Externalref
from .physicals import Storageformat


class Document(Baseobject):
    _tablename:str = 'documents'
    _prefix:str = 'docu'
    _columnlist:list = [ 'docu_id' ,'docu_name', 'docu_stfo_id', 'docu_reference', 'docu_docu_id']

    def __init__(self,psrcname=None,psrcid=None):
        super().__init__(tablename=self._tablename, prefix=self._prefix
                        ,columnlist = self._columnlist
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
    def updparents(psrcname,pparents):
        for key,val in pparents.items():
            # assume, exactly one child and one parent id
            childid = Externalref.getmodeid(psrcname=psrcname,psrcid=key)
            parentid = Externalref.getmodeid(psrcname=psrcname,psrcid=val)
            if childid is not None and parentid is not None:
                dbDML.exec("""
                    update DOCUMENTS as DOK_C
                    set docu_docu_ID = {}
                    where docu_id = {}
                    """.format(parentid,childid))
    #updparents

    @staticmethod
    def docureference(pdocuid):
        data = dbDML.select("""
        select melt_kurzname typ
                ,mode_enti_id
                ,mode_tabl_id
                ,mode_schn_id
                ,mode_scha_id
                ,mode_attr_id
                ,mode_wrtb_id
                ,mode_rela_id
                ,mode_orge_id
                ,mode_buru_id
         from  DOKUMENTE
         join MODELELEM_docu on MODO_docu_ID = docu_ID
         join modellelement on mode_id = MODO_MODE_ID
         join modellelem_typ on melt_id = mode_melt_id
        where docu_id = {}
        """.format(pdocuid))
        retval = []
        if data is None or len(data) == 0: return
        for d in data:
            if d[0] == 'ENTI': pass #o = Entity().getbyid(d[1])
            elif d[0] == 'TABL': o = Tabelle().getbyid(d[2])
            elif d[0] == 'INTF': o = Schnittstelle().getbyid(d[3])
            elif d[0] == 'INTF': pass #o = SchnittstelleAttribut().getbyid(d[4])
            elif d[0] == 'ATTR': pass #o = Attribute().getbyid(d[5])
            elif d[0] == 'DOMA': pass #o = Domain().getbyid(d[6])
            elif d[0] == 'BEZI': pass #o = Beziehung().getbyid(d[7])
            elif d[0] == 'ORGU': pass #o = Organisationseinheit().getbyid(d[8])
            elif d[0] == 'BURU': pass #o = BusinessRule().getbyid(d[9])
            retval.append((d[0],o))
        #for
        return retval
    #docureference

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
            join (select schn_id,tabl_id
                  from tabellen
                  join schnittstellen on SCHN_ID = TABL_SCHN_ID
                 ) on MODO_MODE_ID = SCHN_ID      
            ) 
        where ref_id = {}  
        order by upper(docu_name)
        )
        """.format(pid))
        return docus

    @staticmethod
    def doculist():
        return Document.select(porderby='docu_name')
    #doculist

    """def xxdocureferenced(prelaid=None,pwebenti=None,pwebattr=None):
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
       ) ".format (prelaid,pwebenti,pwebattr))
    return data
#docureferenced
"""
#Document

class ModelelemDocu(Baseobject):
    _tablename:str = 'mode_docu'
    _prefix:str = 'modo'
    _columnlist:list = [ 'modo_id' ,'modo_docu_id', 'modo_mode_id']

    def __init__(self):
        super().__init__(tablename=self._tablename, prefix=self._prefix
                        ,columnlist = self._columnlist)

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=ModelelemDocu._tablename
                               , psql="""
CREATE TABLE MODE_DOCU
    (
     MODO_ID INTEGER NOT NULL primary key autoincrement,
     MODO_MODE_ID integer NOT NULL ,
     MODO_DOCU_ID integer NOT NULL
    ,CONSTRAINT MODO_UK UNIQUE (MODO_MODE_ID ASC, MODO_DOCU_ID ASC)
    ,CONSTRAINT MODO_DOCU_FK FOREIGN KEY(     MODO_DOCU_ID)  
        REFERENCES DOCUMENTS(     DOCU_ID )
        ON DELETE CASCADE
    ,CONSTRAINT MODO_MODE_FKv2 FOREIGN KEY    (     MODO_MODE_ID)
            REFERENCES MODELELEMENT   (     MODE_ID )
         ON DELETE CASCADE
    )
"""
        )

    @staticmethod
    def delete():
        Baseobject.delete(ModelelemDocu._tablename)

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

