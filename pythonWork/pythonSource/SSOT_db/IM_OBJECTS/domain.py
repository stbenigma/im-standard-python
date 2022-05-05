from .baseobject import MultilangBaseobject, Baseobject
from .datatype import Datatype
from .interface import Interface
from .languagetext import Languagetext
from .modelelement import Modelelemtype
from .physicals import Storageformat
from SSOT_infra import nvl,nvl2
from SSOT_db.SQL_INFRA import dbDML


class Domain(MultilangBaseobject):
    DERIVED: str = 'DER'
    DOMAIN: str = 'DOM'
    BIN: str = 'BIN'
    GRP: str = 'GRP'
    LOV: str = 'LOV'
    NUM: str = 'NUM'
    TXT: str = 'TXT'
    DAT: str = 'DAT'
    DAY: str = 'DAY'
    HOUR: str = 'HOUR'
    MILlISECOND: str = 'MILlISECOND'
    MINUTE: str = 'MINUTE'
    MONTH: str = 'MONTH'
    QUARTER: str = 'QUARTER'
    SECOND: str = 'SECOND'
    SEMESTER: str = 'SEMESTER'
    WEEK: str = 'WEEK'
    YEAR: str = 'YEAR'
    DRAWING: str = 'DRAWING'
    FILM: str = 'FILM'
    IMAGE: str = 'IMAGE'
    OTHER: str = 'OTHER'
    SOUND: str = 'SOUND'
    TEXT: str = 'TEXT'
    _tablename: str = 'domains'
    _prefix: str = 'doma'
    _idcolname: str = _prefix + '_id'
    _modelemtype=Modelelemtype.DOMA
    _columnlist: list = []
    _defaultorderby = "doma_name"

    def __init__(self, psrcname=None, psrcid=None):

        super().__init__( multilangcols={'doma_name': Languagetext.DOMA_NAME, 'doma_descr': Languagetext.DOMA_DESCR}
                         , pscrid=psrcid
                         , psrcname=psrcname
                         )

    def getname(self, plang=None):
        return self._getsprachval(colname='doma_name', plang=plang)

    def getmodeid(self):
        return self.doma_id
    # getmodeid

    def isderived(self):
        return self.doma_origin == Domain.DERIVED

    def typeinfo(self):
        daty = Datatype().getbyid(self.doma_daty_id)
        typestring = '' if daty is None else daty.daty_name
        if (self.doma_type in (Domain.TXT, Domain.LOV)):
            infoheaders = (
                'Datentyp', 'Max. Länge', 'Syntaxregel',
                'geändert')
            infovalues = (nvl(self.doma_type), nvl(self.doma_txt_maxlng), nvl(self.doma_txt_syntaxrule),
                          nvl(self.doma_uc) + ',' + nvl(self.doma_dc))
            typestring += nvl2(self.doma_txt_maxlng, '', " ({})".format(self.doma_txt_maxlng))
        elif (self.doma_type == Domain.BIN):
            stf = Storageformat().getbyid(self.doma_bin_stfo_id)
            stfname = stf.getname() if stf is not None else ''
            infoheaders = ('Datentyp', 'Inhaltstyp', 'Format',
                           'geändert')
            infovalues = (
                nvl(self.doma_type), self.displcontenttype(), stfname,
                nvl(self.doma_uc) + ',' + nvl(self.doma_dc)
            )
            typestring += " ({}, {})".format(self.displcontenttype(),stfname)
        elif (self.doma_type == Domain.GRP):
            infoheaders = ('Datentyp', 'geändert')
            infovalues = (self.doma_type, nvl(self.doma_uc) + ',' + nvl(self.doma_dc))
        elif (self.doma_type == Domain.NUM):
            infoheaders = (
                'Datentyp', 'Vorkommast.', 'Nachkommast.'
            , 'Rundungseinh.', 'Einheit', 'Min. Wert',
                'Max. Wwert'
            , 'geändert')
            infovalues = (nvl(self.doma_type), nvl(self.doma_num_total_digits), nvl(self.doma_num_fract_digits),
                          nvl(self.doma_num_round_value), nvl(self.doma_num_phyu_id)
                          , nvl(self.doma_num_minvalue), nvl(self.doma_num_maxvalue)
                          , nvl(self.doma_uc) + ',' + nvl(self.doma_dc))
            typestring += " ({}{}{}{})".format(nvl(self.doma_num_total_digits)
                                               , nvl2(self.doma_num_fract_digits, '', ',{}'.format(self.doma_num_fract_digits))
                                               , nvl2(self.doma_num_minvalue, '', '  >= {}'.format(self.doma_num_minvalue))
                                               , nvl2(self.doma_num_maxvalue, '', '  <= {}'.format(self.doma_num_maxvalue)))
        elif (self.doma_type == Domain.DAT):
            infoheaders = (
                'Datentyp', 'Min. Wert', 'Max. Wwert',
                'Granularität'
            , 'geändert')
            infovalues = (nvl(self.doma_type), nvl(self.doma_dat_minvalue), nvl(self.doma_dat_maxvalue),
                          nvl(self.displgranul()),
                          nvl(self.doma_uc) + ',' + nvl(self.doma_dc))
            typestring += " ({}{}{})".format(
                '' if self.doma_dat_granularity is None else ('  Granularity = {}'.format(self.doma_dat_granularity))
                , '' if self.doma_dat_minvalue is None else '  >= {}'.format(self.doma_dat_minvalue)
                , '' if self.doma_dat_maxvalue is None else '  <= {}'.format(self.doma_dat_maxvalue))
        else:
            infoheaders, infovalues, typestring = None, None, ''
        return [infoheaders, infovalues, typestring]
    # typeinfo

    def typestring(self):
        info = self.typeinfo()
        return info[2]

    # typestring

    def basedatatype(self):
        if self.doma_daty_id is None:
            retval =  ''
        else:
            retval = Datatype().getbyid(self.doma_daty_id).daty_name
        #fi
        return retval

    def refattrcnt(self):
        data = dbDML.select("""select count(*) 
                    from attributes where attr_doma_id = {}
                    """.format(self.doma_id))
        return data[0][0]
    # refattrcnt

    def refcolucnt(self):
        data = dbDML.select("""select count(*) 
                    from columns where colu_doma_id = {}
                    """.format(self.doma_id))
        return data[0][0]
    # refattrcnt

    @staticmethod
    def basetype2domatype(pdatybasetype):
        transl = {Datatype.BINARY: Domain.BIN,
                  Datatype.DATETIME: Domain.DAT,
                  Datatype.NUMERIC: Domain.NUM,
                  Datatype.STRING: Domain.TXT
                  }
        return transl[pdatybasetype]


    @classmethod
    def getbyname(cls,pname: str):
        return cls.getbyuk(doma_name=pname)

    @classmethod
    def getunknown(cls):
        dom = Domain.getbyname(pname='Unknown')
        if dom is None or dom.doma_id is None:
            dom = Domain.getbyname(pname='unknown')
        return dom

    @staticmethod
    def _displdatatype(dt):
        anzDT = {Domain.BIN: 'Binär'
            , Domain.GRP: 'Gruppenattribut'
            , Domain.LOV: 'Werteliste'
            , Domain.NUM: 'Numerisch'
            , Domain.TXT: 'Text'
            , Domain.DAT: 'Zeitpunkt'}
        return anzDT[dt]
    # anzDatentyp

    def displdatatype(self):
        return Domain._displdatatype(self.doma_type)

    def displcontenttype(self):
        return Domain._displcontenttype(self.doma_bin_contenttype)

    @staticmethod
    def _displcontenttype(dt):
        anzDT = {Domain.DRAWING: 'Bild'
            , Domain.FILM: 'Film'
            , Domain.IMAGE: 'Grafik'
            , Domain.TEXT: 'Text'
            , Domain.SOUND: 'Ton'
                 }
        if dt in anzDT.keys():
            return anzDT[dt]
        else:
            return 'Andere'
    # displcontenttype

    def displgranul(self):
        return None if self.doma_dat_granularity is None else Domain._displgranul(dt=self.doma_dat_granularity)

    @staticmethod
    def _displgranul(dt):
        anzDT = {
            Domain.YEAR: 'Jahr',
            Domain.MILlISECOND: 'Millisekunde',
            Domain.MINUTE: 'Minute',
            Domain.MONTH: 'Monat',
            Domain.QUARTER: 'Quartal',
            Domain.SECOND: 'Sekunde',
            Domain.SEMESTER: 'Semester',
            Domain.HOUR: 'Stunde',
            Domain.DAY: 'Tag',
            Domain.WEEK: 'Woche'
        }
        return anzDT[dt]
    # displgranul

    def getgroupmembers(self):
        members = DomaingroupMember.select(pwhere=("dgrm_doma_id_group = ?",self.doma_id))
        return members


    @staticmethod
    def fixdomaininterfaces(pinterfacedomains):
        """{doma_id: <filename>}
            domains in non-default file are IM or interface (relationale model) dependent.
           filename = IM_Domains or <relname>_Domains
         """
        interfacename = lambda filename : filename[:-8]
        interfaces = set((pinterfacedomains.values()))
        intf2id = {}
        for filename in interfaces:
            if filename is None: continue
            intf = Interface().getbyuk(intf_name=interfacename(filename))
            #it is either an interface (relational model) or None (= IM)
            intfid = None if intf is None else intf.intf_id
            intf2id[filename] = intfid
        #for
        domainterfaces = [(intf2id[filename],domaid) for domaid,filename in pinterfacedomains.items()]
        if len(domainterfaces) > 0:
            dbDML.execmany(psql="update domains set doma_intf_id = ? where doma_id = ?", recs=domainterfaces)
        return

class DomaingroupMember(Baseobject):
    _tablename: str = 'domaingroup_members'
    _prefix: str = 'dgrm'
    _idcolname: str = _prefix + '_id'
    _modelemtype = Modelelemtype.DGRM
    _columnlist: list = []
    _defaultorderby = "dgrm_name"

    def __init__(self,psrcname=None,psrcid=None ):

        super().__init__(pscrid=psrcid
                         , psrcname=psrcname
                         )


    def getname(self,plang=None):
        return self.dgrm_name
    def getdescr(self,plang=None):
        return self.dgrm_descr

    def getparentid(self):
        return self.dgrm_doma_id_group
    def getparent(self):
        return Domain().getbyid(self.dgrm_doma_id_group)



    @staticmethod
    def updmember(pid,pdomaid):
        lupd = """update domaingroup_members 
            set dgrm_doma_id_member = {} 
            where dgrm_id = {}
        """.format(pdomaid,pid)
        dbDML.exec(lupd)

# DomaingroupMember

class DefaultValue(Baseobject):
    _tablename: str = 'default_values'
    _prefix: str = 'deva'
    _idcolname: str = _prefix + '_id'
    _columnlist: list = []
    _defaultorderby = "deva_sort_order"

    def __init__(self):

        super().__init__()


# DefaultValue
