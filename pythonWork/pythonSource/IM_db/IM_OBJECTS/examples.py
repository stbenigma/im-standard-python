from SSOT_infra import parameters, logmessages
from .baseobject import MultilangBaseobject,UniqueKeyException
from .modelelement import Modelelemtype
from .languagetext import Languagetext
from .language import Language
from .userdefprop import Userdefprop,Userdefpropvalue



class Example(MultilangBaseobject):
    _tablename:str = 'examples'
    _prefix:str = 'expl'
    _idcolname: str = _prefix + '_id'
    _modelemtype = Modelelemtype.EXPL
    _columnlist:list = []
    _defaultorderby = None

    def __init__(self,pvalue=None,pentiid=None,pattrid=None):
        super().__init__(multilangcols={'expl_value': Languagetext.EXPL_VALUE})
        self.expl_value = pvalue
        self.expl_enti_id = pentiid
        self.expl_attr_id = pattrid

    @classmethod
    def getexamples(cls,pmodeid):
        return Example.select(pwhere=(f"(expl_enti_id = ? or expl_attr_id = ?)",pmodeid,pmodeid))


    @staticmethod
    def fillexamples(pdeflngexpls,plngexpls,plngs,pentiid=None,pattrid=None):
        def inslngexample(plngid,pmodeid,pvalue):
            lgtx = Languagetext()
            lgtx.lgtx_attrname = Languagetext.EXPL_VALUE
            lgtx.lgtx_lang_id = plngid
            lgtx.lgtx_mode_id = pmodeid
            lgtx.lgtx_text = pvalue
            lgtx.insert()
            return

        """transfer examples into the example and the language text tables
           {lng:[expl,...],...}"""
        modeid = pentiid if pentiid is not None else pattrid
        newexamples = dict()
        for idx,expl in enumerate(pdeflngexpls):
            example = Example(pvalue=expl, pentiid = pentiid, pattrid = pattrid)

            i = 2  # safeguard for eternal loop
            origvalue = example.expl_value
            while i < 10:
                try:
                    example.insert()
                    break
                except UniqueKeyException:
                    logmessages.writelog("in Example : {} ".format(origvalue))
                    example.expl_value = origvalue + f" ({str(i)})"
                    i += 1
                    if (i == 10): raise Exception("Key-error in examples: see logfile")
                # try
            # while
            newexamples[idx] = example
        #for

        for idx,expl in newexamples.items():
            """do default-lang"""
            deflng = parameters.dbDefaultLang()
            inslngexample(plngid=Language.spraidlookup(deflng), pmodeid=expl.expl_id
                          , pvalue=expl.expl_value)
            for lng in plngs:
                if lng == deflng: continue
                try:
                    lngvalue = plngexpls[lng][idx]
                    inslngexample(pmodeid=expl.expl_id,plngid=Language.spraidlookup(lng)
                                  , pvalue=lngvalue)
                except:
                    pass
            #for
        #for
        return

    @staticmethod
    def transferexpltransl():
        """get all udpr translations for examples except for the default language
           """
        for udpr in Userdefprop.select(pwhere=("udpr_name like ?", '___EXPL_VALUE')):
            langiso2 = udpr.udpr_name[0:2].lower()
            langid = Language().getbyuk(lang_iso_code2=langiso2).getid()
            if langid == Language.liesdeflangid(): continue
            for udpv in Userdefpropvalue.select(pwhere=("udpv_udpr_id = ?", udpr.udpr_id)):
                lgtx = Languagetext()
                lgtx.lgtx_attrname = Languagetext.EXPL_VALUE
                lgtx.lgtx_text = udpv.udpv_value
                lgtx.lgtx_lang_id = langid
                lgtx.lgtx_mode_id = udpv.udpv_mode_id
                lgtx.lgtx_uc = udpv.udpv_uc
                lgtx.lgtx_dc = udpv.udpv_dc
                lgtx.lgtx_um = udpv.udpv_um
                lgtx.lgtx_dm = udpv.udpv_dm
                lgtx.insert()
        #for
        return