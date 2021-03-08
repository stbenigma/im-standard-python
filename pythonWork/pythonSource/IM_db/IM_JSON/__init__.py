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
#json-key: (processorder,baseobjectload, referencesload)
transferprocs = {
 'model': (1,proj2sql,nofunc)
,'languages': (2,langs2sql,nofunc)
,'physicalunits' : (3,physicalunits2sql,phyurefs2sql)
,'datatypes' : (4,datatypes2sql,dtayrefs2sql)
,'storageformats' : (5,storageformats2sql,stforefs2sql)
,'documents': (6,documents2sql, docurefs2sql)
,'orgunits': (7,orgunits2sql, orgurefs2sql)
,'userdefprops': (8,udps2sql, udprefs2sql)
,'entities': (10,entities2sql,entirefs2sql)
,'systems': (11,systems2sql, systrefs2sql)
,'domains': (12,domains2sql, domarefs2sql)
,'attributes': (13,attributes2sql, attrrefs2sql)
,'arcs': (14,arcs2sql, arcsref2sql)
,'relations': (15,relations2sql, relarefs2sql)
,'keys': (16,keys2sql, keysrefs2sql)
,'tables': (21,tables2sql, tablrefs2sql)
,'columns': (22,columns2sql, colurefs2sql)
,'diagrams': (30,diagrams2sql, diagrefs2sql)
,'_imprint_':(99,nofunc,nofunc)
}

