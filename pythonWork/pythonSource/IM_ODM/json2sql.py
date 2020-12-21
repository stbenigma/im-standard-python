# -*- coding: latin-1 -*-
import json
import sqlite3
import sys
from datetime import date

from IM_DB import dbConnect, dbErstelleTables
from IM_OBJECTS import *
from IM_ODM import transferModel
from IM_JSON import *

errcnt: int = 0
warncnt: int = 0
modellang: str = None
languages = {}  # langid:idso2

anker = lambda n, i: None if i is None else n + str(i)
ankerid = lambda a: None if a is None else a[4:]




def error(pmsg, pelem=None):
    global errcnt
    if type(pmsg) in (sqlite3.IntegrityError, sqlite3.DatabaseError, sqlite3.DataError, sqlite3.Error):
        errtype = 'DB-'
    else:
        errtype = ''

    print("***{}ERROR: {}".format(errtype, pmsg))
    if pelem is not None: print("     ", pelem)
    errcnt += 1
    raise Exception("error")


# error

def warning(pmsg):
    global warncnt
    print("WARNING: {}".format(pmsg))
    warncnt += 1

def insudp(pmodeid,pudps):
    if pudps is None: return
    """ "userdefprop": {
            "-file-": {
                "-group-": {
                    "PENTA TabName": null
                },
            },
        },
    """
    for file,jtheme in pudps.items():
        for group,judps in jtheme.items():
            for udpname,udpval in judps.items():
                udpv = Userdefpropvalue(pmodeid=pmodeid,pudprid=Userdefprop.getbyname(udpname),pvalue=udpval)
                try:
                    udpv.insert()
                except Exception as err:
                    error(pmsg=err, pelem=udpv.tostring())
            #for
        #for
    #for



def filllangs(pelem):
    global modellang, languages
    """   "languages": {
      "de": {
         "name": "Deutsch",
         "iso3": "deu",
         "modellanguage": true,
         "replacementlang": null
      }"""
    for iso2, jlang in pelem.items():
        lang = Language()
        lang.lang_iso_code2 = iso2
        lang.lang_iso_code3 = jlang['iso3']
        lang.lang_iso_name = jlang['name']
        lang.lang_uc = None
        lang.lang_dc = date.today()
        lang.lang_is_base_lang = Boolean.bool2str(jlang['modellanguage'])
        if jlang['modellanguage']:
            if modellang is not None:
                error(pmsg="more than one model language defined", pelem=jlang)
            else:
                modellang = lang.lang_iso_code2
            # fi
        # fi
        lang.lang_is_text_lang = Boolean.FALSE
        try:
            langid = lang.insert()
        except Exception as err:
            error(pmsg=err, pelem=lang.tostring())
            continue
        languages[langid] = iso2
    # for
    try:
        Language.setallreplacementlang()
    except Exception as err:
        error(pmsg=err, pelem=pelem)

    if modellang is None:
        error(pmsg="No model language defined", pelem=None)
    # print([l.tostring() for l in Language.select()])

def filludps(pelem):
    for udpranker,judp in pelem.items():
        udpr = Userdefprop(ptheme=judp['theme'],pgroup=judp['group'],pname=judp['name'])
        udpr.udpr_id = ankerid(udpranker)
        try:
            udpr.insert()
        except Exception as err:
            error(pmsg=err, pelem=list(judp))
            continue

        for melttype in judp['usedfor']:
            try:
                ModelelementProperty(pmeltid=Modelelemtype.getbyshortname(melttype).getid(),pudprid=udpr.udpr_id).insert()
            except Exception as err:
                error(pmsg=err, pelem=list(judp))
        #for
    #for



def fillrelas(pelem):
    """      "RELA11990": {
         "name": "Relation_76",
         "type": "M:1",
         "from-to": {
            "enti": "ENTI11889",
            "arc": null,
            "assoc": {
               "de": "ist",
               "en": "is",
               "fr": "est"
            },
            "maptype": "1",
            "hist": false,
            "mandatory": false,
            "cardstr": "1..N"
         },
         "to-from": {
            "enti": "ENTI11909",
            "arc": "ARCS12031",
            "assoc": {
               "de": "definiert",
               "en": "defines",
               "fr": "d\u00e9finit"
            },
            "maptype": "M",
            "hist": false,
            "mandatory": true,
            "cardstr": "0..1"
         },
         "isinkeys": [],
         "uc": "stb",
         "dc": "2019-05-07 12:07:04 UTC",
         "um": null,
         "dm": null
      },"""
    for janker, jrela in pelem.items():
        rela = Relation()
        rela.rela_id = ankerid(janker)
        rela.rela_name = jrela['name']
        rela.rela_type = jrela['type']
        rela.rela_enti_id_from = ankerid(jrela['from-to']['enti'])
        rela.rela_arcs_id_from = ankerid(jrela['from-to']['arc'])
        rela.rela_assoc_from_to = jrela['from-to']['assoc'][modellang]
        rela.rela_maptype_from_to = jrela['from-to']['maptype']
        rela.rela_mandatory_from_to = Boolean.bool2str(jrela['from-to']['mandatory'])
        rela.rela_hist_from_to = Boolean.bool2str(jrela['from-to']['hist'])
        rela.rela_enti_id_to = ankerid(jrela['to-from']['enti'])
        rela.rela_arcs_id_to = ankerid(jrela['to-from']['arc'])
        rela.rela_assoc_to_from = jrela['to-from']['assoc'][modellang]
        rela.rela_maptype_to_from = jrela['to-from']['maptype']
        rela.rela_mandatory_to_from = Boolean.bool2str(jrela['to-from']['mandatory'])
        rela.rela_hist_to_from = Boolean.bool2str(jrela['to-from']['hist'])
        rela.rela_uc = jrela['uc']
        rela.rela_dc = jrela['dc']
        rela.rela_um = jrela['um']
        rela.rela_dm = jrela['dm']


def fillsql(pmodel):
    global errcnt, warncnt
    for eletyp, elem in pmodel.jsmodel.items():
        if eletyp == 'model':
            proj2sql(elem)
        elif eletyp == 'entities':
            entities2sql(pmodel=pmodel)
        elif eletyp == 'languages':
            filllangs(elem)
        elif eletyp == 'userdefprop':
            filludps(elem)
        elif eletyp == 'attributes':
            attributes2sql(pmodel=pmodel)
        elif eletyp == 'relations':
            fillrelas(elem)
        elif eletyp == 'languages':
            filllangs(elem)
        else:
            warning('Unknown elementtype "{}" ignored'.format(eletyp))
    # for
    if errcnt > 0:
        print("==== {} error(s) found ====".format(str(errcnt)))
    if warncnt > 0:
        print("==== {} warning(s) found ====".format(str(warncnt)))
# fillsql


# Main Programm
def main(pjsonin, pdbout):
    model = JSModel.readfromfile(pfilename=pjsonin)

    if pdbout is None:
        dbConnect.openDB(p_filepath="file::memory:?cache=shared");
    else:
        dbConnect.openDB(pdbout, 'ON');

    dbErstelleTables.erstelleInfra();
    transferModel.insertBaseData(pwithlangs=False)

    try:
        fillsql(pmodel=model)
    finally:
        print("JSON file {} filled into db {}"
              .format(pjsonin, "in-memory" if pdbout is None else pdbout))
# main


if __name__ == '__main__':
    main(pjsonin=sys.argv[1],
         pdbout=None if len(sys.argv) <= 2 else sys.argv[2])
