from SSOT_db.IM_JSON import *
from SSOT_db.IM_OBJECTS import BusinessruleElement, Modelelemtype, \
    Modelelement, Boolean, BusinessRule, Externalref


""" get the list of json-buru-id's fot the element with pelemid"""
def buruinelements(pelemid=None):
    if pelemid is None:
        retval = []
    else:
        bures = BusinessruleElement.select(pwhere=("bure_mode_id = ?", pelemid))
        retval = [jsguid(Modelelemtype.BURU, be.bure_buru_id) for be in bures]
    return retval


def buruelement2js(pbure=None):
    if pbure is None:
        retval = {'r/w': 'R'}
    else:
        retval = {"r/w": "W" if Boolean.str2bool(pbure.bure_writeable) else "R"}
    return retval


def buruelements2js(pbures=None):
    if pbures is None:
        retval = {'xxxx0000': buruelement2js()}
    else:
        retval = dict()
        for bure in pbures:
            mode = Modelelement().getbyid(bure.bure_mode_id)
            retval[jsguid(mode.mode_type, mode.mode_id)] = buruelement2js(bure)
    return retval

def businessrule2js(pburu, plangs={'en'}):
    model = ['name', 'descr', 'level', 'type',
             'impact', 'rule', 'errormsg', 'elements',
             'uc', 'dc', 'um', 'dm',
             'sourceref'
             ]
    if pburu is None:
        retval = fillmodel(pmodel=model,
                           pentries=[multilangtext(), multilangtext(),
                                     '', '', '', '',
                                     multilangtext(),
                                     [buruelements2js()],
                                     '', '', '', '', sourceref()
                                     ]
                           )
    elif pburu.buru_id is None:
        # not read from DB new record (assume no translation of texts)
        retval = fillmodel(pmodel=model,
                           pentries=[{l: pburu.buru_name for l in plangs}, {l: pburu.buru_descr for l in plangs},
                                     pburu.buru_level, pburu.buru_type, pburu.buru_impact, pburu.buru_rule,
                                     {l: pburu.buru_errormsg for l in plangs},
                                     [buruelements2js()],
                                     pburu.buru_uc, pburu.buru_dc, pburu.buru_um, pburu.buru_dm,
                                     sourceref({pburu.getsrcname(): [pburu.getsrcid(), '']})
                                     ]
                           )
    else:
        retval = fillmodel(pmodel=model,
                           pentries=[multilangtext(pburu.buru_name_l),
                                     multilangtext(pburu.buru_descr_l),
                                     pburu.buru_level, pburu.buru_type,
                                     pburu.buru_impact, pburu.buru_rule,
                                     multilangtext(pburu.buru_errormsg_l),
                                     buruelements2js(pburu.getchildren()),
                                     pburu.buru_uc, pburu.buru_dc, pburu.buru_um, pburu.buru_dm,
                                     Externalref.getsrcinfo(pmodeid=pburu.buru_id),
                                     ]
                           )
    # fi
    return retval

def businessrules2js(pemptymodel):
    if pemptymodel:
        burus = {jsguid(Modelelemtype.BURU, '0000'): businessrule2js(None)}
    else:
        burus = {jsguid(Modelelemtype.BURU, b.buru_id): businessrule2js(b) for b in BusinessRule.select()}
    return burus

def js2buru(pkey, pelem, psrcname=None, psrcid=None, pmodellang=None):
    buru = BusinessRule(srcname=psrcname, srcid=psrcid,
                        buru_id=jsguid2id(pkey),
                        buru_name=pelem['name'][pmodellang],
                        buru_errormsg=pelem['errormsg'][pmodellang],
                        buru_descr=pelem['descr'][pmodellang],
                        buru_level=pelem['level'],
                        buru_type=pelem['type'],
                        buru_rule=pelem['rule'],
                        buru_impact=pelem['impact'],
                        buru_uc=pelem['uc'],
                        buru_dc=pelem['dc'],
                        buru_um=pelem['um'],
                        buru_dm=pelem['dm'],
                        )
    return buru

def insbures(presult: Mergeresult, pburuid, prefs):
    """ "elements": {
            "ATTR165": {
               "r/w": "R"
            }
         },
    """
    inscnt = 0
    delcnt = BusinessruleElement.delete(pwhere=("bure_buru_id = ?", pburuid))
    for refid, val in prefs.items():
        modeid = jsguid2id(refid)
        bure = BusinessruleElement(bure_buru_id=pburuid,
                                   bure_mode_id=modeid,
                                   bure_writeable=val["r/w"] == 'W'
                                   )
        try:
            bure.insert()
            inscnt += 1
        except Exception as err:
            presult.markdberror(perr=err, pelem=[refid, pburuid])
            continue
    # for
    presult.addinscnt(max(0, (inscnt - delcnt)))
    presult.adddelcnt(max(0, (delcnt - inscnt)))
    return

def businessrules2sql(presult: Mergeresult, podmjson: JSModel, pwithextsrcref):
    fromodm2db(presult=presult, podmjson=podmjson, pelemtype=Modelelemtype.BURU, pjs2obj=js2buru,
               pwithextsrcref=pwithextsrcref)
    """             "BURU166": {
         "name": {
            "de": "Personenrolle.BESCHREIBUNG_CHECK",
            "en": "*de* Personenrolle.BESCHREIBUNG_CHECK",
            "fr": "*de* Personenrolle.BESCHREIBUNG_CHECK"
         },
         "descr": {
            "de": "dbtype=Generic Constraint    rule=Beschreibung = \"Geografische Einheit\".\"Geoinformation\"",
            "en": "*de* dbtype=Generic Constraint    rule=Beschreibung = \"Geografische Einheit\".\"Geoinformation\"",
            "fr": "*de* dbtype=Generic Constraint    rule=Beschreibung = \"Geografische Einheit\".\"Geoinformation\""
         },
         "level": "ATTR",
         "type": "CHECK",
         "impact": "REFUSE",
         "rule": "Beschreibung = \"Geografische Einheit\".\"Geoinformation\"",
         "errormsg": {
            "de": "Rule None violated.",
            "en": "*de* Rule None violated.",
            "fr": "*de* Rule None violated."
         },
         "elements": {
            "ATTR165": {
               "r/w": "R"
            }
         },
         "uc": "sys",
         "dc": "2022-04-16 13:16:52.213213",
         "um": null,
         "dm": null,
         "sourceref": {
            "ODM": [
               "116DF002-EA64-1985-173B-A197A3118F61check",
               "2022-04-16 13:16:52.214382"
            ]
         }
      },"""
    for jid, jelem in podmjson.getelements(pelemtype=Modelelemtype.BURU).items():
        buruid = keytransl(jid)
        if buruid is None: continue  # element was not treated
        replacelgtx(presult=presult, pmodeid=buruid, pattr=Languagetext.BURU_DESCR, ptexts=jelem['descr'])
        replacelgtx(presult=presult, pmodeid=buruid, pattr=Languagetext.BURU_ERRORMSG, ptexts=jelem['errormsg'])
        replacelgtx(presult=presult, pmodeid=buruid, pattr=Languagetext.BURU_NAME, ptexts=jelem['name'])
        insbures(presult=presult, pburuid=buruid, prefs=jelem['elements'])
        inssourceref(presult=presult, pmodeid=buruid, psources=jelem["sourceref"])
    # for
