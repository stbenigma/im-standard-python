from .baseobject import Baseobject, MultilangBaseobject
from .modellelement import Modellelement
from .sprachtext import Sprachtext

class Attribut(MultilangBaseobject):
    _tablename: str = 'attributes'
    _prefix: str = 'attr'
    _columnlist: list = ['attr_id', 'attr_enti_id', 'attr_bezi_id',
                         'attr_wrtb_id', 'attr_tech_name', 'attr_anzname',
                         'attr_tooltip', 'attr_beschr', 'attr_business_rule',
                         'attr_anz_rhflg', 'attr_deskriptor', 'attr_pflichtattr',
                         'attr_historisiert', 'attr_wiederholt', 'attr_sprachabhaengig',
                         'attr_verschluesselt', 'attr_odm_guid', 'attr_uc',
                         'attr_dc', 'attr_um', 'attr_dm']

    def __init__(self, pname=None, pentiid=None, prelaid=None):
        super().__init__(tablename=Attribut._tablename, prefix=Attribut._prefix
                         , columnlist=Attribut._columnlist
                         , multilangcols={'attr_anzname': Sprachtext.ATTR_NAME,
                                          'attr_beschr': Sprachtext.ATTR_COMMENT})
        self.attr_anzname = pname
        self.attr_enti_id = pentiid
        self.attr_bezi_id = prelaid

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Attribut._tablename
                               , psql="""
CREATE TABLE attributes(
    attr_id                integer NOT NULL primary key autoincrement,
    attr_enti_id           integer ,
    attr_bezi_id           integer,
    attr_wrtb_id           integer NOT NULL,
    attr_tech_name         varchar(60)NOT NULL,
    attr_anzname   varchar(100) ,
    attr_tooltip   varchar(100) ,
    attr_beschr    varchar(2000) ,
    attr_business_rule     varchar(4000),
    attr_anz_rhflg         integer ,
    attr_deskriptor        varchar(5) default 'FALSE' NOT NULL
        CHECK(attr_deskriptor IN(
            'FALSE',
            'TRUE'
        )),
    attr_pflichtattr       varchar(5) default 'FALSE' NOT NULL
        CHECK(attr_pflichtattr IN(
            'FALSE',
            'TRUE'
        )),
    attr_historisiert      varchar(5) default 'FALSE' NOT NULL
        CHECK(attr_historisiert IN(
            'FALSE',
            'TRUE'
        )),
    attr_wiederholt        varchar(5) default 'FALSE' NOT NULL
        CHECK(attr_wiederholt IN(
            'FALSE',
            'TRUE'
        )),
    attr_sprachabhaengig   varchar(5) default 'FALSE' NOT NULL
        CHECK(attr_sprachabhaengig IN(
            'FALSE',
            'TRUE'
        )),
    attr_verschluesselt    varchar(5) default 'FALSE' NOT NULL
        CHECK(attr_verschluesselt IN(
            'FALSE',
            'TRUE'
        )),
    attr_odm_guid		varchar(36),	
    attr_uc                varchar(30 )NOT NULL,
    attr_dc                varchar(30 ),
    attr_um                varchar(30),
    attr_dm                varchar(30 ),
    UNIQUE(attr_enti_id, attr_tech_name),
	CONSTRAINT attr_arc_fk CHECK((attr_enti_id is null and attr_bezi_id is not null) 
								or (attr_enti_id is not null and attr_bezi_id is null)),
 	CONSTRAINT attr_enti_fk FOREIGN KEY(attr_enti_id)
        REFERENCES entitaeten(enti_id),
	CONSTRAINT attr_wrtb_fk	FOREIGN KEY(attr_wrtb_id)        
			REFERENCES wertebereiche(wrtb_id),
	CONSTRAINT attr_bezi_fk FOREIGN KEY(attr_bezi_id)
		        REFERENCES beziehungen(bezi_id)
)
        """)

    def webanker(self,pmodelid=None):
        return super().webanker(pmodelid)

    def getname(self, plang=None):
        return self._getsprachval(colname='attr_name', plang=plang)

    def getentiname(self, plang=None):
        return Entitaet().getbyid(self.attr_enti_id).getname(plang)

    def getmodellelement(self):
        return Modellelement.getbyelemid(pattrid=self.attr_id)

    def getmodeid(self):
        return self.getmodellelement().mode_id

    def getparent(self):
        return Entitaet.getbyid(self.attr_enti_id)

    @staticmethod
    def delete():
        Baseobject.delete(Attribut._tablename)

    @staticmethod
    def select(pwhere=None, porderby="attr_anz_rhflg"):
        attrs = Baseobject.select(pclass=Attribut
                                  , pwhere=pwhere, porderby=porderby)
        return attrs
    # select
# Attribut
from .entitaet import Entitaet




