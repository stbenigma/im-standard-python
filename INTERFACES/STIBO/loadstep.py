import json
import logging
import re
from pathlib import Path

import xmltodict

from IM_STANDARD import nvl, alwayslist
from INTERFACES.STIBO.mygraph import Graph


class LoadStep:
    """
    reads and parses a xml file (or all xmlfiles in the parentpath
    in case of multiple files, debugoutput can be written per file to debugpath
    """
    DEFAULTATTRGROUP = "Step Attributes"
    DEFAULTOBJECTGROUP = "Step Objects"

    def __init__(self,
                 stepfilepath,
                 rootusertypes="^.+$",
                 debugpath=None):
        self.stepfilepath = stepfilepath

        self.models = dict()
        self.attrgroups = list()
        self.attributes = list()
        self.lovgroups = list()
        self.lovs = list()
        self.allusertypes = list()
        self.edgetypes = list()
        self.xreftypes = dict()

        self.xmls = dict()
        self.readmodels(inpath=stepfilepath,
                        debugpath=debugpath)
        for filename, xmljson in self.xmls.items():
            self.parsexml(filename=filename, xmljson=xmljson)

        self.myusertypes = self.restrictusertypes(rootusertypes)
        self.removeinconsistencies()
        return

    def readmodels(self, inpath: Path, debugpath):
        """

        @param inpath:
            file or parentpath. reading one file or all *.xml files in parentpath
        @param debugpath:
            debug outputpath for intermediate jsonfiles
        @return: self.xmls[filestem] for every file that was read
        """

        def readxml(infile):
            """ reads the file from infile
                returns json version of it
            """
            with open(infile) as f:
                xmlcontent = f.read()
                xml = xmltodict.parse(xmlcontent)
            return xml

        def writedebug(debugpath: Path, name: str, struct: dict):
            if debugpath is not None:
                with open(debugpath / (name + ".json"), "w") as outf:
                    json.dump(struct, outf, indent=2)
            return

        if inpath.is_file():
            self.xmls[inpath.stem] = readxml(infile=inpath)
            writedebug(debugpath=debugpath,
                       name=inpath.stem,
                       struct=self.xmls[inpath.stem])
        elif inpath.is_dir():
            for onepath in inpath.iterdir():
                if onepath.suffix == '.xml' and not onepath.stem.startswith("~"):
                    self.xmls[onepath.stem] = readxml(infile=onepath)
                    writedebug(debugpath=debugpath,
                               name=onepath.stem,
                               struct=self.xmls[onepath.stem])
        else:
            raise Exception(f"parentpath must be file or directory {inpath.__str__()}")
        return

    def restrictusertypes(self, rootusertypes):
        """
        @rootusertypes: regexp to filter root usertypes
        @return: usertypes filtered from allusertypes
        """
        # restrict to _children of my root(s)
        myids = set()
        roots = set()
        # do roots
        for ut in self.allusertypes:
            myid = ut.get("ID")
            if re.match(rootusertypes, myid):
                roots.add(myid)
        myids.update(roots)

        # add decendants of chosen roots
        for root in roots:
            myids.update(self._utgraph().get_descendants(root))

        retval = [ut for ut in self.allusertypes if ut.get("ID") in myids]
        return retval

    def removeinconsistencies(self):
        """
        remove all nonexistent references and show warning / error
        @return:
        """
        # all usertypes referencing a nonexistent usertype
        allknownUTids = [myut.get("ID") for myut in self.myusertypes]
        for myut in self.myusertypes:
            if myut.get("PATH")[0] not in allknownUTids:
                logging.warning(f'UserType {myut.get("ID")} references nonexistent usertype {myut.get("PATH")[0]}')
                myut["PATH"] = [self.DEFAULTOBJECTGROUP] + myut["PATH"][1:]
                del myut['UserTypeLink']

        for xreftype,xrefs in self.xreftypes.items():
            for xref in xrefs:
                if xref.get("PATH")[0] not in allknownUTids:
                    logging.warning(f'Crossref {xref.get("ID")} references nonexistent usertype {xref.get("PATH")[0]}')
                    xref["PATH"] = [self.DEFAULTOBJECTGROUP] + xref["PATH"][1:]

        # remove relations with nonexistent usertypes
        for xreftype, xrefs in self.xreftypes.items():
            for xref in xrefs:
                for sourcetarget in ("TargetUserTypeLink", "UserTypeLink"):
                    newlist=[]
                    for source in xref.get(sourcetarget, []):
                        sourceid = self._getanyid(elem=source, anyid="@UserTypeID")
                        if sourceid in allknownUTids:
                            newlist.append({"@UserTypeID":sourceid})
                        else:
                            logging.info(f'userType reference {sourceid} not in known userTypes ')
                    xref[sourcetarget] = newlist

            # remove all xrefs with no target or source
            self.xreftypes[xreftype]=[xref for xref in xrefs
               if len(xref.get("TargetUserTypeLink",[])) > 0 and
                      len(xref.get("UserTypeLink",[])) > 0]

        #remove all unmatched Attribute/group links
        alllovsids=[lov.get("ID") for lov in self.lovs]
        allgrpsids=[grp.get("ID") for grp in self.attrgroups]
        for attr in self.attributes:
            lovids = [self._getanyid(elem=lov,anyid="@ListOfValueID")
                      for lov in attr.get("ListOfValueLink",[])]
            if len(lovids)>0:
                if lovids[0] not in alllovsids:
                    logging.warning(f'LOV "{lovids[0]}" in "{attr.get("ID")}" does not exist')
                    del attr["ListOfValueLink"]

            agrids = [self._getanyid(elem=attrgr, anyid="@AttributeGroupID")
                      for attrgr in attr.get("AttributeGroupLink", [])]
            attrgrpids=[]
            for agrid in agrids:
                if agrid not in allgrpsids:
                    logging.warning(f'Attributegroup "{agrid}" in "{attr.get("ID")}" does not exist')
                else:
                    attrgrpids.append(agrid)

            if len(attrgrpids)==0 and "AttributeGroupLink" in attr:
                del attr["AttributeGroupLink"]
            else:
                attr["AttributeGroupLink"]=[{"@AttributeGroupID":agrid} for agrid in attrgrpids]

        return

    def _utpath(self, utid):
        """ get the path from thiw usertype up to the root (with no parent"""
        retval = []
        if utid is None: return retval
        ut = self.getelement(elements=self.allusertypes, idval=utid)
        if ut is not None:
            parents = alwayslist(ut.get("UserTypeLink"))
            if len(parents) > 0:
                parentid = self._getanyid(elem=parents[0], anyid="@UserTypeID")
                if parentid == utid:
                    # stop recursion
                    logging.warning(f"{utid} refers itself as utlink parent")
                else:
                    retval = self._utpath(parentid)
        retval += [utid]
        return retval

    def parsexml(self, filename: str, xmljson: dict):
        stepmodelname = next(iter(xmljson))
        content = xmljson[stepmodelname]
        self.models.setdefault(stepmodelname, dict())
        self.models[stepmodelname].setdefault("exporttime", content.get("@ExportTime"))

        attrgroupslist = content.get("AttributeGroupList")
        if attrgroupslist is not None:
            for attrgroup in alwayslist(attrgroupslist.get("AttributeGroup")):
                self.doinattrgroup(groups=self.attrgroups,
                                   stepmodelname=stepmodelname,
                                   attrgroup=attrgroup,
                                   source=filename,
                                   parent=None,
                                   parentpath=[],
                                   grouptype="AttributeGroup")

        attrlist = content.get("AttributeList")
        if attrlist is not None:
            for attr in alwayslist(attrlist.get("Attribute")):
                path = self._attrgrppath(attr) + [attr.get("@ID")]
                self.attributes.append(self.doinelement(elem=attr,
                                                        source=filename,
                                                        stepmodelname=stepmodelname,
                                                        path=path
                                                        ))

        lovgroupslist = content.get("ListOfValuesGroupList")
        if lovgroupslist is not None:
            for lovgroup in alwayslist(lovgroupslist.get("ListOfValuesGroup")):
                self.doinattrgroup(groups=self.lovgroups,
                                   stepmodelname=stepmodelname,
                                   attrgroup=lovgroup,
                                   source=filename,
                                   parent=None,
                                   parentpath=[],
                                   grouptype="ListOfValuesGroup")

        lovlist = content.get("ListsOfValues")
        if lovlist is not None:
            for lov in alwayslist(lovlist.get("ListOfValue")):
                group = self.getelement(elements=self.lovgroups, idval=lov.get("@ParentID"))
                self.lovs.append(self.doinelement(elem=lov,
                                                  stepmodelname=stepmodelname,
                                                  source=filename,
                                                  path=group.get("PATH") + [lov.get("@ID")]
                                                  ))

        utlist = content.get("UserTypes")
        if utlist is not None:
            for ut in alwayslist(utlist.get("UserType")):
                self.allusertypes.append(self.doinelement(elem=ut,
                                                          stepmodelname=stepmodelname,
                                                          source=filename,
                                                          path=None)
                                         )
            for ut in self.allusertypes:
                ut["PATH"] = self._utpath(self._getanyid(elem=ut, anyid="@ID"))

        etlist = content.get("EdgeType")
        if etlist is not None:
            for et in alwayslist(etlist):
                self.edgetypes.append(self.doinelement(elem=et,
                                                       stepmodelname=stepmodelname,
                                                       source=filename,
                                                       path=[]
                                                       ))

        xreflist = content.get("CrossReferenceTypes")
        if xreflist is not None:
            for xreftype, xref in xreflist.items():
                self.xreftypes.setdefault(xreftype, [])
                for onexref in alwayslist(xref):
                    onerefpath = self._xrefpath(onexref)
                    if onerefpath is None:
                        # skip non existing targets or links
                        continue
                    self.xreftypes[xreftype].append(
                        self.doinelement(elem=onexref,
                                         stepmodelname=stepmodelname,
                                         source=filename,
                                         path=onerefpath + [xreftype,
                                                            self._getanyid(elem=onexref,
                                                                           anyid="@ID")]
                                         ))

        return

    @staticmethod
    def _getelements(elements, idval, field="ID"):
        found = [elem for elem in elements if elem.get(field) == idval]
        return found

    def getelement(self, elements, idval, field="ID"):
        elems = self._getelements(elements=elements,
                                  idval=idval, field=field)
        if len(elems) == 0:
            return None
        elif len(elems) == 1:
            return elems[0]
        else:
            assert False, f"Element with agrid {idval} found more than once"

    def doinattrgroup(self, groups, stepmodelname,
                      attrgroup, source,
                      parent, parentpath,
                      grouptype):
        agrid = self._getanyid(elem=attrgroup, anyid="@ID")
        mypath = parentpath + [agrid]
        if self.getelement(elements=groups, idval=agrid) is not None:
            logging.warning(f"Duplicate {grouptype} {agrid} from source {source}")
        else:
            group = {"name": attrgroup.get("Name"),
                     "ID": agrid,
                     "PARENT": parent,
                     "MODEL": stepmodelname,
                     "SOURCE": source,
                     "PATH": mypath
                     }
            groups.append(group)

        children = alwayslist(attrgroup.get(grouptype))
        for subattrgroup in children:
            self.doinattrgroup(groups=groups,
                               stepmodelname=stepmodelname,
                               attrgroup=subattrgroup,
                               parent=agrid,
                               source=source,
                               parentpath=mypath,
                               grouptype=grouptype)
        return

    @staticmethod
    def doinelement(elem, stepmodelname,
                    source, path):
        elementry = {key.lstrip("@"): val if type(val) in [str] else alwayslist(val)
                     for key, val in elem.items()}
        elementry["MODEL"] = stepmodelname
        elementry["SOURCE"] = source
        elementry["PATH"] = path
        return elementry

    @staticmethod
    def _getanyid(elem, anyid):
        """
        @param elem: element with a id
        @param anyid: id probably starting with @
        @return:
            elem with anyid
            or elem with anyid.lstrip("@")
            or None if nothing found
        """
        if anyid in elem:
            return elem.get(anyid)
        elif type(anyid) == str and anyid.lstrip("@") in elem:
            return elem.get(anyid.lstrip("@"))
        else:
            return None

    def _xrefpath(self, xref):
        """

        @param xref: xrefelement
        @return: path of first targeuusertpye or usertype
            "DefaultCollection" if both are empty
        """
        if "TargetUserTypeLink" in xref:
            utid = self._getanyid(elem=alwayslist(xref.get("TargetUserTypeLink"))[0],
                                  anyid="@UserTypeID")
            ut = self.getelement(elements=self.allusertypes, idval=utid)
            if ut is None:
                logging.warning(f"{utid} in crossreference TargetUserTypeLink does not exist")
                retval = None
            else:
                retval = ut.get("PATH")
        elif "UserTypeLink" in xref:
            utid = self._getanyid(elem=alwayslist(xref.get("UserTypeLink"))[0],
                                  anyid="@UserTypeID")
            ut = self.getelement(elements=self.allusertypes, idval=utid)
            if ut is None:
                logging.warning(f"{utid} in crossreference UserTypeLink does not exist")
                retval = None
            else:
                retval = ut.get("PATH")
        else:
            retval = [self.DEFAULTOBJECTGROUP]
        return retval

    def _attrgrppath(self, elem):
        if "AttributeGroupLink" in elem:
            attrgrplinks = alwayslist(elem.get("AttributeGroupLink"))
            attrgroupid = nvl(attrgrplinks[0].get('@AttributeGroupID'),
                              attrgrplinks[0].get('AttributeGroupID')
                              )
            attrgroup = self.getelement(elements=self.attrgroups, idval=attrgroupid)
            if attrgroup is None:
                attrpath = [self.DEFAULTATTRGROUP]
            else:
                attrpath = alwayslist(attrgroup.get("PATH"))

        # get first group as collection
        else:
            attrpath = [self.DEFAULTATTRGROUP]
            # TODO check für subattribute alwayslist(elem.get("PATH"))[1:-1]
        return attrpath

    def _utgraph(self):
        g = Graph()
        for ut in self.allusertypes:
            for ut2 in alwayslist(ut.get("UserTypeLink")):
                if ut.get("ID") != self._getanyid(elem=ut2,
                                                  anyid="@UserTypeID"):
                    g.add_edge(self._getanyid(elem=ut2, anyid="@UserTypeID"),
                               self._getanyid(elem=ut, anyid="@ID"))
        return g
