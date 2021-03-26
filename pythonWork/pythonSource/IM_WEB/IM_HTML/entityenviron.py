from IM_JSON import JSModel

"""defines the classes and functions to implement an entity-environment representation"""
nvl = lambda str: str if str is not None else ''

class EntityCell():
    def __init__(self,pentiid=None,pentiname=None,passoc=None):
        self.setentiid(pentiid)
        self.setentiname(pentiname)
        self.setassoc(passoc)

    def getentiid(self):
        return self._entiid

    def setentiid(self,pentiid):
        self._entiid = pentiid

    def getentiname(self):
        return self._entiname

    def setentiname(self,pentiname):
        self._entiname = pentiname

    def getassoc(self):
        return self._assoc
    def setassoc(self,passoc):
        self._assoc = passoc

    def __str__(self):
        return ', '.join ((nvl(self.getentiid()),nvl(self.getentiname()),nvl(self.getassoc())))


class EntityEnvironment():
    ROLE = 'role'
    SUPER = 'super'
    PARENT = 'parent'
    CHILD = 'child'

    """Dictrionary for one entity.
        two-dimensional etensible grid 1. index (hidx)  -> left to right, 2. index (vidx) top down
        0/0 is the center
        1,2,3 are cells to downwards or to the right
        -1,-2,-3 are cells upwards or to the left
        {  ...
          ,-1 : {}   HIDX
          ,0 : {...
                ,-1 :  VIDX
                ,0 : [entiid,entiname,relationtext]
                ,1 :
                ...}
          ,1 : {}
          ,...}
    """
    def __init__(self,pentiid,pentiname):
        self._grid = dict()
        self.fillcell (phidx=0,pvidx=0,pcell=EntityCell(pentiid=pentiid,pentiname=pentiname))
        return

    def fillcell(self,phidx,pvidx,pcell:EntityCell):
        if phidx not in self._grid.keys():
            self._grid[phidx] = {}
        self._grid[phidx][pvidx] = pcell

    def getcell (self,phidx,pvidx):
        if phidx not in self._grid.keys():
            return EntityCell() #non existing cell is empty
        if pvidx not in  self._grid[phidx].keys():
            return EntityCell()
        return self._grid[phidx][pvidx]

    def getminhkey(self):
        return min(self._grid.keys())
    def getmaxhkey(self):
        return max(self._grid.keys())

    def getminvkey(self):
        return min(min(vkey for vkey in cols.keys()) for cols in self._grid.values())
    def getmaxvkey(self):
        return max(max(vkey for vkey in cols.keys()) for cols in self._grid.values())

    def getentiid(self, phidx, pvidx):
        cell = self.getcell(phidx=phidx, pvidx=pvidx)
        if len(cell) == 0:
            return None
        else:
            return cell.getentiid()

    def getentiname(self, phidx, pvidx):
        cell = self.getcell(phidx=phidx, pvidx=pvidx)
        if len(cell) == 0:
            return None
        else:
            return cell.getentiname()

    def getassoc(self, phidx, pvidx):
        cell = self.getcell(phidx=phidx, pvidx=pvidx)
        if len(cell) == 0:
            return None
        else:
            return cell.getassoc()

    def togrid(self,pentities: list, ptype, pjson, pmodellang,passoc=None):
        doubleline = len(pentities) > 2
        if ptype == EntityEnvironment.ROLE:
            hidx, vidx = 1, 0
        elif ptype == EntityEnvironment.SUPER:
            hidx, vidx = -1, 0
        elif ptype == EntityEnvironment.PARENT:
            hidx, vidx = -1, -1
        elif ptype == EntityEnvironment.CHILD:
            hidx, vidx = 1, 1
        else:
            assert false, "illegal type '{}'".format(ptype)

        entities: dict = pjson.getelements(pelemtype=Modelelemtype.ENTI)
        for entiid in pentities:
            self.fillcell(pvidx=hidx, phidx=vidx,
                          pcell=EntityCell(pentiid=entiid, pentiname=entities[entiid]['name'][pmodellang], passoc=passoc))
            hidx = switchhidx(hidx, doubleline)
            vidx += 1 if ptype in (EntityEnvironment.CHILD, EntityEnvironment.SUPER) else -1
        # for
        return

    def togrid2(self,pcells: list, ptype):
        doubleline = len(pcells) > 2
        if ptype == EntityEnvironment.ROLE:
            hidx, vidx = 1, 0
        elif ptype == EntityEnvironment.SUPER:
            hidx, vidx = -1, 0
        elif ptype == EntityEnvironment.PARENT:
            hidx, vidx = -1, -1
        elif ptype == EntityEnvironment.CHILD:
            hidx, vidx = 1, 1
        else:
            assert false, "illegal type '{}'".format(ptype)

        for cell in pcells:
            self.fillcell(pvidx=hidx, phidx=vidx,pcell=cell)
            hidx = switchhidx(hidx, doubleline)
            vidx += 1 if ptype in (EntityEnvironment.CHILD, EntityEnvironment.SUPER) else -1
        # for
        return

"""switch to second line for next entity"""
sign = lambda x: (1, -1)[x<0]
switchhidx = lambda hidx,doubleline:  1*sign(hidx) if ((abs(hidx) == 2) or not doubleline) else  2*sign(hidx)

def related(pentiid,prelated,pjson,pcardinality,pmodellang):
    retval = []
    entities:dict = pjson.getelements(pelemtype=Modelelemtype.ENTI)
    for relaid in prelated:
        rela = pjson.getelements(pelemtype=Modelelemtype.RELA)[relaid]
        if rela['type'] in (Relation.ISAROLE, Relation.ISASUBTYPE): continue
        if (rela['from-to']['enti'] == pentiid
            and rela['to-from']['maptype'] == pcardinality):
            parentid=rela['to-from']['enti']
            assoc = rela['from-to']['assoc'][pmodellang]
        elif (rela['to-from']['enti'] == pentiid
            and rela['from-to']['maptype'] == pcardinality):
            parentid = rela['from-to']['enti']
            assoc = rela['to-from']['assoc'][pmodellang]
        else:
            continue # not my relation or I am not a child
        #fi
        retval.append(EntityCell(pentiid=parentid, pentiname=entities[parentid]['name'][pmodellang],passoc=assoc))
    #for
    return retval

def createentienvironment(pentiid,pjson:JSModel,pmodellang):

    """creates an EntityEnvironment for the given entity found in the json-structure"""
    entities:dict = pjson.getelements(pelemtype=Modelelemtype.ENTI)

    if not pentiid in entities.keys(): return None #non existing entity is Nothing

    entienvir = EntityEnvironment(pentiid=pentiid,pentiname=entities[pentiid]['name'][pmodellang])
    entienvir.togrid(pentities= entities[pentiid]['roles+'] + entities[pentiid]['subtypes+'],ptype=EntityEnvironment.ROLE,pjson=pjson,pmodellang=pmodellang)
    entienvir.togrid(pentities= entities[pentiid]['supertypes+'],ptype=EntityEnvironment.SUPER,pjson=pjson,pmodellang=pmodellang)

    """handle Parents (I am ONE, parent is MANY)"""
    parents = related(pentiid=pentiid,prelated=entities[pentiid]['relations+'], pjson=pjson, pcardinality=Relation.ONE, pmodellang=pmodellang)
    entienvir.togrid2(pcells=parents,ptype=EntityEnvironment.PARENT)

    """handle children (I am MANY, Child is ONE or MANY)"""
    children = related(pentiid=pentiid,prelated=entities[pentiid]['relations+'], pjson=pjson, pcardinality=Relation.MANY, pmodellang=pmodellang)
    entienvir.togrid2(pcells=children,ptype=EntityEnvironment.CHILD)

    return entienvir


from IM_OBJECTS import Modelelemtype,Relation





