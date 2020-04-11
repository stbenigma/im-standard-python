from IM_DB import dbDML

from .baseobject import Baseobject


class Dokument(Baseobject):
    _tablename:str = 'dokumente'
    _prefix:str = 'doku'
    _columnlist:list = [ 'doku_id' ,'doku_name', 'doku_format', 'doku_referenz', 'doku_doku_id', 'doku_odm_guid', 'doku_parent_odm_guid' ]

    def __init__(self):
        super().__init__(tablename=self._tablename, prefix=self._prefix
                        ,columnlist = self._columnlist)
        ?? hier die Kinder und Eltern lesen, falls der ID gesetzt ist (= gelesen!)

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Dokument._tablename
                               , psql="""
            CREATE TABLE DOKUMENTE 
				      (
				       DOKU_ID integer primary key autoincrement,
				       DOKU_NAME VARCHAR (60) NOT NULL , 
				       DOKU_FORMAT VARCHAR (20) , 
				       DOKU_REFERENZ VARCHAR (500) , 
				       DOKU_DOKU_ID NUMERIC (10),	
					   DOKU_ODM_GUID varchar(36),
					   DOKU_PARENT_ODM_GUID varchar(36),  
			   CONSTRAINT DOKU_UK UNIQUE (DOKU_ID),
			   CONSTRAINT DOKU_DOKU_FK FOREIGN KEY (DOKU_DOKU_ID) 
			   				      REFERENCES DOKUMENTE ( DOKU_ID )ON DELETE CASCADE
				      )
				"""
                            )

    def webanker(self):
        return super().webanker()

    @staticmethod
    def delete():
        Baseobject.delete(Dokument._tablename)

    @staticmethod
    def select(pwhere=None, porderby=None):
        return Baseobject.select(pclass=Dokument
                                 , pwhere=pwhere, porderby=porderby)
    @staticmethod
    def indexlist():
        data = Dokument.select(porderby='doku_name')
        indexlist = [[d.doku_name,d.webanker(),d.doku_id] for d in data]
        return indexlist
    #indexlist

    @staticmethod
    def updparents():
        dbDML.exec("""
            update Dokumente as DOK_C
            set DOKU_DOKU_ID = (
            select DOK_P.DOKU_ID from Dokumente as DOK_P
            where DOK_P.DOKU_ODM_GUID = DOK_C.DOKU_PARENT_ODM_GUID)
            """)
    #updparents

    @staticmethod
    def dokureference(pdokuid):
        data = dbDML.select("""
        select melt_kurzname typ
                ,mode_enti_id
                ,mode_tabl_id
                ,mode_schn_id
                ,mode_scha_id
                ,mode_attr_id
                ,mode_wrtb_id
                ,mode_bezi_id
                ,mode_orge_id
                ,mode_buru_id
         from  DOKUMENTE
         join MODELELEM_DOKU on MODO_DOKU_ID = DOKU_ID
         join modellelement on mode_id = MODO_MODE_ID
         join modellelem_typ on melt_id = mode_melt_id
        where doku_id = {}
        """.format(pdokuid))
        retval = []
        if data is None or len(data) == 0: return
        for d in data:
            if d[0] == 'ENTI': pass #o = Entitaet().getbyid(d[1])
            elif d[0] == 'TABL': o = Tabelle().getbyid(d[2])
            elif d[0] == 'SCHN': o = Schnittstelle().getbyid(d[3])
            elif d[0] == 'SCHA': pass #o = Schnittstelle().getbyid(d[3])
            elif d[0] == 'ATTR': pass #o = Schnittstelle().getbyid(d[3])
            elif d[0] == 'WRTB': pass #o = Schnittstelle().getbyid(d[3])
            elif d[0] == 'BEZI': pass #o = Schnittstelle().getbyid(d[3])
            elif d[0] == 'ORGE': pass #o = Schnittstelle().getbyid(d[3])
            elif d[0] == 'BURU': pass #o = Schnittstelle().getbyid(d[3])
            retval.append((d[0],o))
        #for
    return retval
    #dokureference

    @staticmethod
    def dokulist():
        docs = Dokument.select(porderby='doku_name'):

        data = dbDML.select("""
            select child.DOKU_ID,child.DOKU_NAME,child.DOKU_FORMAT,child.DOKU_REFERENZ
             ,parent.DOKU_ID parent_id ,parent.doku_name parent_name
             ,(select group_concat(grandchild.doku_id||':'||grandchild.doku_name, '|') kinder
                from DOKUMENTE grandchild
                where grandchild.DOKU_DOKU_ID = child.DOKU_ID) kinder
            from DOKUMENTE child
            left join dokumente parent on parent.DOKU_ID = child.DOKU_DOKU_ID
            order by upper(child.doku_name)
            """.format(p_lang))
        return data
    #dokulist

    """def xxdokureferenced(pbeziid=None,pentiid=None,pattrid=None):
    data = dbDML.select("
    select child.doku_id, child.DOKU_NAME,child.DOKU_FORMAT,child.DOKU_REFERENZ
       ,parent.DOKU_ID parent_id,parent.DOKU_NAME parent_name
 from  DOKUMENTE child
left join dokumente parent on parent.DOKU_ID = child.DOKU_DOKU_ID  
join MODELELEM_DOKU on MODO_DOKU_ID = child.DOKU_ID
join modellelement on mode_id = MODO_MODE_ID
where  (   mode_bezi_id = {}
        or mode_enti_id = {}
        or mode_attr_id = {}
       ) ".format (pbeziid,pentiid,pattrid))
    return data
#dokureferenced
"""
#Dokument

class ModelelemDoku(Baseobject):
    _tablename:str = 'modelelem_doku'
    _prefix:str = 'modo'
    _columnlist:list = [ 'modo_id' ,'modo_doku_id', 'modo_mode_id']

    def __init__(self):
        super().__init__(tablename=self._tablename, prefix=self._prefix
                        ,columnlist = self._columnlist)

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=ModelelemDoku._tablename
                               , psql="""
				  create table modelelem_doku 
				      (
				       modo_id integer primary key autoincrement,
				       modo_doku_id numeric (10) not null , 
				       modo_mode_id numeric (10) not null,
					   constraint modo_un unique (modo_doku_id , modo_mode_id),
					   constraint modo_doku_fk foreign key (modo_doku_id) 
					   				      references dokumente ( doku_id )on delete cascade
				  constraint modo_mode_fk foreign key (modo_mode_id) 
				      references modellelement (mode_id)   on delete cascade
			      )
                """
                )

    def webanker(self):
        return super().webanker()

    @staticmethod
    def delete():
        Baseobject.delete(ModelelemDoku._tablename)

    @staticmethod
    def select(pwhere=None, porderby=None):
        return Baseobject.select(pclass=ModelelemDoku
                                 , pwhere=pwhere, porderby=porderby)
    @staticmethod
    def insertdokuref(pdocguidlist,pmodeid):
        if pdocguidlist is None: return
        for docguid in pdocguidlist:
            modo = ModelelemDoku()
            modo.modo_doku_id = Dokument().getID(docguid)
            modo.modo_mode_id = pmodeid
            modo.insert()
        #for
    #insertdokuref

#ModelelemDoku

