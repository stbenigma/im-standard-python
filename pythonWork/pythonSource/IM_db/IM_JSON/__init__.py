#__all__ = [""]
from .jsbase import *
from .jsreference import *
from .jslang import inslgtx,langs2js,langs2sql,js2lang
from .jsrefdata import *
from .jsentity import entities2js,entities2sql,entirefs2sql
from .jsdomain import domaingroupmembers,domains2js,domarefs2sql,domains2sql
from .jsattribute import attributes2js,keys2js,attributes2sql,attrrefs2sql,keys2sql,keysrefs2sql
from .jsrelation import relations2js,arcs2js,relations2sql,relarefs2sql,arcs2sql,arcsref2sql
from .jsdiagram import diagrams2js,defarcs,diagrefs2sql,diagrams2sql
from .jssystem import systems2js,systems2sql,systrefs2sql
from .jstable import tables2js,tablrefs2sql,tables2sql
from .jscolumn import columns2js,columns2sql,colurefs2sql
from .jsmodel import *

nofunc = lambda p : None
#json-key: (processorder,baseobjectload, referencesload,js2obj,hasexternalref)
transferprocs = {
 'model': (1,proj2sql,nofunc,js2proj,False)
,'languages': (2,langs2sql,nofunc,js2lang,False)
,'physicalunits' : (3,physicalunits2sql,phyurefs2sql,js2phyu,False)
,'datatypes' : (4,datatypes2sql,dtayrefs2sql,js2daty,True)
,'storageformats' : (5,storageformats2sql,stforefs2sql,js2stfo,False)
,'documents': (6,documents2sql, docurefs2sql,js2docu,True)
,'orgunits': (7,orgunits2sql, orgurefs2sql,js2orgu,True)
,'userdefprops': (8,udps2sql, udprefs2sql,nofunc,True)
,'systems': (10,systems2sql, systrefs2sql,nofunc,True)
,'domains': (12,domains2sql, domarefs2sql,nofunc,True)
,'entities': (14,entities2sql,entirefs2sql,nofunc,True)
,'attributes': (16,attributes2sql, attrrefs2sql,nofunc,True)
,'arcs': (18,arcs2sql, arcsref2sql,nofunc,True)
,'relations': (20,relations2sql, relarefs2sql,nofunc,True)
,'keys': (22,keys2sql, keysrefs2sql,nofunc,True)
,'tables': (30,tables2sql, tablrefs2sql,nofunc,True)
,'columns': (32,columns2sql, colurefs2sql,nofunc,True)
,'diagrams': (34,diagrams2sql, diagrefs2sql,nofunc,True)
,'_imprint_':(99,nofunc,nofunc,nofunc,True)
}
