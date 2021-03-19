from IM_DB import *
from .baseobject import MultilangBaseobject, Baseobject
from .datatype import Datatype
from .interface import Interface
from .languagetext import Languagetext
from .modelelement import Modelelemtype
from .physicals import Storageformat


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
    _columnlist: list = []
    __unknowndom = None

    def __init__(self, psrcname=None, psrcid=None):
        if (len(Domain._columnlist) == 0): Domain._columnlist = Baseobject.gettablecolumns(Domain._tablename)
        super().__init__(tablename=Domain._tablename, prefix=Domain._prefix
                         , multilangcols={'doma_name': Languagetext.DOMA_NAME, 'doma_descr': Languagetext.DOMA_DESCR}
                         , pmodelemtype=Modelelemtype.DOMA
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
                Languagetext.transl('Datentyp'), Languagetext.transl('Max. Länge'), Languagetext.transl('Syntaxregel'),
                Languagetext.transl('geändert'))
            infovalues = (parameters.nvl(self.doma_type), parameters.nvl(self.doma_txt_maxlng), parameters.nvl(self.doma_txt_syntaxrule),
                          parameters.nvl(self.doma_uc) + ',' + parameters.nvl(self.doma_dc))
            typestring += parameters.nvl2(self.doma_txt_maxlng,''," ({})".format(self.doma_txt_maxlng))
        elif (self.doma_type == Domain.BIN):
            stf = Storageformat().getbyid(self.doma_bin_stfo_id)
            stfname = stf.getname() if stf is not None else ''
            infoheaders = (Languagetext.transl('Datentyp'), Languagetext.transl('Inhaltstyp'), Languagetext.transl('Format'),
                           Languagetext.transl('geändert'))
            infovalues = (
                parameters.nvl(self.doma_type), self.displcontenttype(), stfname,
                parameters.nvl(self.doma_uc) + ',' + parameters.nvl(self.doma_dc)
            )
            typestring += " ({}, {})".format(self.displcontenttype(),stfname)
        elif (self.doma_type == Domain.GRP):
            infoheaders = (Languagetext.transl('Datentyp'), Languagetext.transl('geändert'))
            infovalues = (self.doma_type, parameters.nvl(self.doma_uc) + ',' + parameters.nvl(self.doma_dc))
        elif (self.doma_type == Domain.NUM):
            infoheaders = (
                Languagetext.transl('Datentyp'), Languagetext.transl('Vorkommast.'), Languagetext.transl('Nachkommast.')
            , Languagetext.transl('Rundungseinh.'), Languagetext.transl('Einheit'), Languagetext.transl('Min. Wert'),
                Languagetext.transl('Max. Wwert')
            , Languagetext.transl('geändert'))
            infovalues = (parameters.nvl(self.doma_type), parameters.nvl(self.doma_num_total_digits), parameters.nvl(self.doma_num_fract_digits),
                          parameters.nvl(self.doma_num_round_value), parameters.nvl(self.doma_num_phyu_id)
                          , parameters.nvl(self.doma_num_minvalue), parameters.nvl(self.doma_num_maxvalue)
                          , parameters.nvl(self.doma_uc) + ',' + parameters.nvl(self.doma_dc))
            typestring += " ({}{}{}{})".format(parameters.nvl(self.doma_num_total_digits)
                                                 , parameters.nvl2(self.doma_num_fract_digits,'', ',{}'.format(self.doma_num_fract_digits))
                                                 , parameters.nvl2(self.doma_num_minvalue,'', '  >= {}'.format(self.doma_num_minvalue))
                                                 , parameters.nvl2(self.doma_num_maxvalue,'', '  <= {}'.format(self.doma_num_maxvalue)))
        elif (self.doma_type == Domain.DAT):
            infoheaders = (
                Languagetext.transl('Datentyp'), Languagetext.transl('Min. Wert'), Languagetext.transl('Max. Wwert'),
                Languagetext.transl('Granularität')
            , Languagetext.transl('geändert'))
            infovalues = (parameters.nvl(self.doma_type), parameters.nvl(self.doma_dat_minvalue), parameters.nvl(self.doma_dat_maxvalue),
                          parameters.nvl(self.displgranul()),
                          parameters.nvl(self.doma_uc) + ',' + parameters.nvl(self.doma_dc))
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

    @staticmethod
    def select(pwhere=None, porderby="doma_name"):
        wrtbs = Baseobject.select(pclass=Domain
                                  , pwhere=pwhere, porderby=porderby)
        return wrtbs
    # select

    @staticmethod
    def delete(pwhere=None):
        return Baseobject.delete(Domain._tablename)


    @staticmethod
    def getbyname(pname: str):
        return Domain().getbyuk(doma_name=pname)

    @staticmethod
    def getunknown():
        if Domain.__unknowndom is None:
            dom = Domain.getbyname(pname='Unknown')
            if dom is None or dom.doma_id is None:
                dom = Domain.getbyname(pname='unknown')
            # fi
            Domain.__unknowndom = dom
        # fi
        return Domain.__unknowndom
    # getunknown

    @staticmethod
    def _displdatatype(dt,plang=None):
        anzDT = {Domain.BIN: Languagetext.transl('Binär', plang=plang)
            , Domain.GRP: Languagetext.transl('Gruppenattribut', plang=plang)
            , Domain.LOV: Languagetext.transl('Werteliste', plang=plang)
            , Domain.NUM: Languagetext.transl('Numerisch', plang=plang)
            , Domain.TXT: Languagetext.transl('Text', plang=plang)
            , Domain.DAT: Languagetext.transl('Zeitpunkt', plang=plang)}
        return anzDT[dt]
    # anzDatentyp

    def displdatatype(self,plang=None):
        return Domain._displdatatype(self.doma_type,plang=plang)

    def displcontenttype(self,plang=None):
        return Domain._displcontenttype(self.doma_bin_contenttype)

    @staticmethod
    def _displcontenttype(dt,plang=None):
        anzDT = {Domain.DRAWING: Languagetext.transl('Bild', plang=plang)
            , Domain.FILM: Languagetext.transl('Film', plang=plang)
            , Domain.IMAGE: Languagetext.transl('Grafik', plang=plang)
            , Domain.TEXT: Languagetext.transl('Text', plang=plang)
            , Domain.SOUND: Languagetext.transl('Ton', plang=plang)
                 }
        if dt in anzDT.keys():
            return anzDT[dt]
        else:
            return Languagetext.transl('Andere', plang=plang)
    # displcontenttype

    def displgranul(self,plang=None):
        return None if self.doma_dat_granularity is None else Domain._displgranul(dt=self.doma_dat_granularity,plang=plang)

    @staticmethod
    def _displgranul(dt,plang=None):
        anzDT = {
            Domain.YEAR: Languagetext.transl('Jahr', plang=plang),
            Domain.MILlISECOND: Languagetext.transl('Millisekunde', plang=plang),
            Domain.MINUTE: Languagetext.transl('Minute', plang=plang),
            Domain.MONTH: Languagetext.transl('Monat', plang=plang),
            Domain.QUARTER: Languagetext.transl('Quartal', plang=plang),
            Domain.SECOND: Languagetext.transl('Sekunde', plang=plang),
            Domain.SEMESTER: Languagetext.transl('Semester', plang=plang),
            Domain.HOUR: Languagetext.transl('Stunde', plang=plang),
            Domain.DAY: Languagetext.transl('Tag', plang=plang),
            Domain.WEEK: Languagetext.transl('Woche', plang=plang)
        }
        return anzDT[dt]
    # displgranul

    def getgroupmembers(self):
        members = Domain.select(pwhere="doma_id in (select dgrm_doma_id_member from domaingroup_members where dgrm_doma_id_group = {})".format(self.doma_id))


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
            intfid = None if intf is None else intf.intf_id
            intf2id[filename] = intfid
        #for
        domainterfaces = [(intf2id[filename],domaid) for domaid,filename in pinterfacedomains.items()]
        if len(domainterfaces) > 0:
            dbDML.execmany(psql="update domains set doma_intf_id = ? where doma_id = ?",recs=domainterfaces)
# Domain

class DomaingroupMember(Baseobject):
    _tablename: str = 'domaingroup_members'
    _prefix: str = 'dgrm'
    _columnlist: list = []

    def __init__(self,psrcname=None,psrcid=None ):
        if (len(DomaingroupMember._columnlist) == 0): DomaingroupMember._columnlist = Baseobject.gettablecolumns(DomaingroupMember._tablename)
        super().__init__(tablename=DomaingroupMember._tablename, prefix=DomaingroupMember._prefix
                         , pmodelemtype=Modelelemtype.DGRM
                         , pscrid=psrcid
                         , psrcname=psrcname
                         )


    def getname(self,plang=None):
        return self.dgrm_name
    def getdescr(self,plang=None):
        return self.dgrm_descr

    @staticmethod
    def delete(pwhere=None):
        return Baseobject.delete(DomaingroupMember._tablename,pwhere=pwhere)

    @staticmethod
    def select(pwhere=None, porderby="dgrm_name"):
        return Baseobject.select(pclass=DomaingroupMember
                                 , pwhere=pwhere, porderby=porderby)

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
    _columnlist: list = []

    def __init__(self):
        if (len(DefaultValue._columnlist) == 0): DefaultValue._columnlist = Baseobject.gettablecolumns(DefaultValue._tablename)
        super().__init__(tablename=DefaultValue._tablename, prefix=DefaultValue._prefix)

    @staticmethod
    def delete(pwhere=None):
        return Baseobject.delete(DefaultValue._tablename,pwhere=pwhere)

    @staticmethod
    def select(pwhere=None, porderby="deva_sort_order"):
        return Baseobject.select(pclass=DefaultValue
                                 , pwhere=pwhere, porderby=porderby)

# DefaultValue
