from IM_DB import dbDML
from .baseobject import Baseobject
from .modelelement import Modelelemtype,Modelelement
from .externalref import Externalref
from .physicals import Storageformat


class OragnisationalUnit(Baseobject):
    _tablename:str = 'organisationalunits'
    _prefix:str = 'orgu'
    _columnlist:list = [ 'orgu_id' ,'orgu_name', 'orgu_descr', 'orgu_mail'
                        , 'orgu_telefon','orgu_address', 'orgu_orgu_id'
                         ,'orgu_uc','orgu_dc','orgu_um','orgu_dm']

    def __init__(self,psrcname=None,psrcid=None):
        super().__init__(tablename=self._tablename, prefix=self._prefix
                        ,columnlist = self._columnlist
                         ,pmodelemtype=Modelelemtype.ORGU
                         ,pscrid=psrcid
                         ,psrcname=psrcname
                         )

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=OragnisationalUnit._tablename
                               , psql="""
CREATE TABLE organisationalunits(
   orgu_id       integer primary key,
   orgu_name     VARCHAR(60)NOT NULL,
   orgu_descr     VARCHAR(4000),
   orgu_mail     VARCHAR(200)NULL,
   orgu_telefon  VARCHAR(30)NULL,
   orgu_address  VARCHAR(4000)NULL,
   orgu_orgu_id  NUMBER(10)NULL,
   orgu_uc             varchar(30) not null,
   orgu_dc             varchar(30) not null,
   orgu_um             varchar(30),
   orgu_dm             varchar(30)
   ,CONSTRAINT orgu_email_un UNIQUE(orgu_mail)
   ,CONSTRAINT orgu_name_un UNIQUE(orgu_name)
   ,CONSTRAINT orgu_mode_fk FOREIGN KEY(orgu_id)
              REFERENCES modelelement(mode_id)
                  ON DELETE CASCADE
	,CONSTRAINT orgu_orgu_fk FOREIGN KEY(orgu_orgu_id)
       REFERENCES organisationalunits(orgu_id)
   )"""
        )

    def getname(self,plang=None):
        return self.orgu_name

    def getparent(self):
        return Document().getbyid(self.orgu_orgu_id)
    #getparent

    def getchildren(self):
        return Document.select(pwhere='orgu_orgu_id = {}'.format(self.orgu_id)
                                              , porderby= 'orgu_name')
    #getchildren

    @staticmethod
    def delete():
        Baseobject.delete(OragnisationalUnit._tablename)

    @staticmethod
    def select(pwhere=None, porderby=None):
        return Baseobject.select(pclass=OragnisationalUnit
                                 , pwhere=pwhere, porderby=porderby)
    @staticmethod
    def updparents(psrcname,pparents):
        for key,val in pparents.items():
            # assume, exactly one child and one parent id
            childid = Externalref.getmodeid(psrcname=psrcname,psrcid=key)
            parentid = Externalref.getmodeid(psrcname=psrcname,psrcid=val)
            if childid is not None and parentid is not None:
                dbDML.exec("""
                    update organisationalunits as ou_C
                    set orgu_orgu_ID = {}
                    where orgu_id = {}
                    """.format(parentid,childid))
    #updparents



    def getrefmodes(self,pmelttype=None):
        return  Modelelement.select(
                pwhere="""mode_id in 
                            (select mode_id 
                            from mode_orgu 
                            join modelelement on mode_id = moou_mode_id
                            where moou_orgu_id = {}
                            and mode_type like '{}')"""
                    .format(self.orgu_id,pmelttype if pmelttype is not None else '%'))

    @staticmethod

    def orgulist():
        return OrganisationalUnit.select(porderby='orgu_name')
    #orgulist
#OragniastionalUnit

class ModelelemOrgu(Baseobject):
    _tablename:str = 'mode_orgu'
    _prefix:str = 'moou'
    _columnlist:list = [ 'moou_id' ,'moou_orgu_id', 'moou_mode_id']

    def __init__(self):
        super().__init__(tablename=self._tablename, prefix=self._prefix
                        ,columnlist = self._columnlist)

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=ModelelemOrgu._tablename
                               , psql="""
CREATE TABLE mode_orgu(
    moou_id       integer primary key,
    moou_mode_id  integer NOT NULL,
    moou_orgu_id  integer NOT NULL
	,CONSTRAINT moou_orgu_fk FOREIGN KEY(moou_orgu_id)
           REFERENCES organisationalunits(orgu_id)
               ON DELETE CASCADE
	,CONSTRAINT moou_mode_fk FOREIGN KEY(moou_mode_id)
           REFERENCES modelelement(mode_id)
			  ON DELETE CASCADE
)
"""
        )

    @staticmethod
    def delete():
        Baseobject.delete(ModelelemOrgu._tablename)

    @staticmethod
    def select(pwhere=None, porderby=None):
        return Baseobject.select(pclass=ModelelemOrgu
                                 , pwhere=pwhere, porderby=porderby)
    @staticmethod
    def insertorguref(porguguidlist,pmodeid):
        if porguguidlist is None: return
        for orguguid in porguguidlist:
            moou = ModelelemOrgu()
            moou.moou_orgu_id = Externalref.getODMmodeid(psrcid=orguguid)
            moou.moou_mode_id = pmodeid
            moou.insert()
        #for
    #insertdocuref
#ModelelemDoku

