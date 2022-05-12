from SSOT_db.IM_OBJECTS import Language, Entity, BusinessRule, Attribute, Domain, Relation, Modelelemtype
from SSOT_db.SQL_INFRA import dbConnect
from .langexceldata import Langexceldata

class Exportdata:
    ENTI, BURU, ATTR, DOMA, RELA, EXPL, SYNO = (
     Modelelemtype.ENTI, Modelelemtype.BURU, Modelelemtype.ATTR, Modelelemtype.DOMA, Modelelemtype.RELA,
     Modelelemtype.EXPL, Modelelemtype.SYNO)
    ELEMTYPES = (ENTI, BURU, ATTR, DOMA, RELA)# the others (syno,expl) are only weak entities

    def __init__(self, pdbfile):
        self._data = dict()
        self._readlangs()
        for elemtype in self.ELEMTYPES:
            self._data[elemtype] = self.gatherdata(ptype=elemtype)
        else:
            dbConnect.closeDB()

    def _readlangs(self):
        self._langs = self._langs = [l.lang_iso_code2 for l in Language.select(porderby='lang_is_base_lang desc,lang_iso_code2')]

    def getlangs(self):
        return self._langs

    def fulldata(self, ptext: dict, pdesc: str, pcomment: str) -> dict:
        retval = ptext
        retval['descr'] = pdesc
        retval['comment'] = pcomment
        return retval

    def xlskey(self, ptype: str, pid: int, pattr: str):
        return ptype + '-' + str(pid) + '-' + pattr

    def getdata(self, ptype=None):
        if ptype is None:
            retval = dict()
            for elemtype in self._data.keys():
                retval.update(self._data[elemtype])
            else:
                return retval

        assert ptype in self._data.keys(), f"{ptype} is no key for data"
        return self._data[ptype]

    def _readentidata(self):
        elemtype = self.ENTI
        elements = Entity.select()
        data = dict()
        for elem in elements:
            data[self.xlskey(elemtype, elem.enti_id, 'name')] = self.fulldata(elem.enti_name_l, elem.enti_name + '  - Name', '')
            data[self.xlskey(elemtype, elem.enti_id, 'descr')] = self.fulldata(elem.enti_descr_l, elem.enti_name + '  - Description', '')
            data[self.xlskey(elemtype, elem.enti_id, 'tooltip')] = self.fulldata(elem.enti_tooltip_l, elem.enti_name + '  - Tooltip', '')

        for syno in elem.getsynonyms():
            data[self.xlskey(self.SYNO, syno.syno_id, 'synonyms')] = self.fulldata(syno.syno_name_l, elem.enti_name + '  - Synonym', '')
        else:
            for expl in elem.getexamples():
                data[self.xlskey(self.EXPL, expl.expl_id, 'examples')] = self.fulldata(expl.expl_value_l, elem.enti_name + '  - Example', '')
            else:
                return data

    def _readburudata(self):
        elemtype = self.BURU
        elements = BusinessRule.select()
        data = dict()
        for elem in elements:
            data[self.xlskey(elemtype, elem.buru_id, 'name')] = self.fulldata(elem.buru_name_l, elem.buru_name + '  - Name', '')
            data[self.xlskey(elemtype, elem.buru_id, 'descr')] = self.fulldata(elem.buru_descr_l, elem.buru_name + '  - Description', '')
            data[self.xlskey(elemtype, elem.buru_id, 'errormsg')] = self.fulldata(elem.buru_errormsg_l, elem.buru_name + '  - Errormessage', '')
        else:
            return data

    def _readattrdata(self):
        elemtype = self.ATTR
        elements = Attribute.select()
        data = dict()
        for elem in elements:
            data[self.xlskey(elemtype, elem.attr_id, 'name')] = self.fulldata(elem.attr_displ_name_l, elem.attr_tech_name + '  - Name', '')
            data[self.xlskey(elemtype, elem.attr_id, 'descr')] = self.fulldata(elem.attr_descr_l, elem.attr_tech_name + '  - Description', '')
            data[self.xlskey(elemtype, elem.attr_id, 'tooltip')] = self.fulldata(elem.attr_tooltip_l, elem.attr_tech_name + '  - Errormessage', '')
            for expl in elem.getexamples():
                data[self.xlskey(self.EXPL, expl.expl_id, 'examples')] = self.fulldata(expl.expl_value_l, elem.attr_tech_name + '  - Example', '')
            else:
                return data

    def _readdomadata(self):
        elemtype = self.DOMA
        elements = Domain.select()
        data = dict()
        for elem in elements:
            data[self.xlskey(elemtype, elem.doma_id, 'name')] = self.fulldata(elem.doma_name_l, elem.doma_name + '  - Name', '')
            data[self.xlskey(elemtype, elem.doma_id, 'descr')] = self.fulldata(elem.doma_descr_l, elem.doma_name + '  - Description', '')
        else:
            return data

    def _readreladata(self):
        elemtype = self.RELA
        elements = Relation.select()
        data = dict()
        for elem in elements:
            fromentiname = elem.getfromentity().enti_name
            toentiname = elem.gettoentity().enti_name
            data[self.xlskey(elemtype, elem.rela_id, 'fromto')] = self.fulldata(elem.rela_assoc_from_to_l, fromentiname + ' => ' + toentiname, '')
            data[self.xlskey(elemtype, elem.rela_id, 'tofrom')] = self.fulldata(elem.rela_assoc_to_from_l, toentiname + ' => ' + fromentiname, '')
        else:
            return data

    def gatherdata(self, ptype: str):
        if ptype == self.ENTI:
            return self._readentidata()
        if ptype == self.ATTR:
            return self._readattrdata()
        if ptype == self.DOMA:
            return self._readdomadata()
        if ptype == self.RELA:
            return self._readreladata()
        if ptype == self.BURU:
            return self._readburudata()
        print(f"***** {ptype} is unknown element")
        return dict()
