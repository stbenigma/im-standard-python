from IM_STANDARD import nvl


class JsonElement:
    """ all functions to create standard json structures"""

    ELEMENT_TYPES={"Entity":"name",
                   "Domain":"name",
                   "Category":"name",
                   "Attribute":"name",
                   "BusinessRule":None,
                   "System":"name",
                   "Column":"name",
                   "Relation":None
                   }
    def __init__(self, **kwargs):
        self.data = kwargs
        self.elemtype = "undefined"
        return

    def __getitem__(self, attribute_name):
        """
        Enables bracket notation access (person['name']).
        Relies on getattr() internally.
        """
        return self.data.get(attribute_name)

    def setproperty(self, propname, val):
        """ sets value into the datastructure of this element"""
        self.data[propname] = val

    def __str__(self):
        return f"{self.elemtype}:{nvl(self.data.get('label'),nvl(self.data.get('name')))}"


    ##### General functions
    @staticmethod
    def optionalprop(destobject, propname, value, intvalue=None):
        """sets a value into a json structure as propname if
           the value is not empty (None, "", [], {})
           if intvalue: value is set as integer, not as string
          """
        if not (value is None or value == "" or
                (type(value) in (list, dict) and len(value) == 0)):
            # property is only set, if it is not null or not empty
            if type(destobject) == dict:
                destobject[propname] = int(float(value)) if intvalue else value
            elif type(destobject) == list:
                destobject.append({propname: int(float(value)) if intvalue else value})
            else:
                raise Exception(f"unkown type to add property {type(destobject)}")
        return

    def addoptionalprop(self, propname, value, intvalue=None):
        """sets a value into a json structure as propname if
           the value is not empty (None, "", [], {})
           if intvalue: value is set as integer, not as string
          """
        JsonElement.optionalprop(destobject=self.data,
                                 propname=propname,
                                 value=value,
                                 intvalue=intvalue)

        return

    def getadditionalprops(self):
        return self.data.get("additionalProps", dict())

    def getadditionalprop(self, name):
        return self.getadditionalprops().get(name)

    def getid(self):
        return self.data.get("elementid", None)

    def getname(self):
        nameprop=self.ELEMENT_TYPES[self.elemtype]
        if nameprop is not None:
            return self.data.get(nameprop)
        else:
            if self.elemtype=="Relation":
                #build name for relation
                #TODO translate further up
                return self.data["fwd"].get("assoctext") + "->" + self.data["bwd"].get("assoctext")

    @staticmethod
    def filterprops(props):
        """
        @param props: dictionary with properties to be filtered for emtpy entries
        @return: dictionary with all properties which are not empty (None, "", [], {}
                None if props is None
        """
        if props is None:
            retval = None
        else:
            retval = dict()
            for key, val in props.items():
                JsonElement.optionalprop(destobject=retval,
                                         propname=key,
                                         value=val
                                         )
        return retval

    def add_restprops(self, fields, **kwargs):
        """
        add all values of kwargs beeing in fields to the jsonstruct (as optional elements).
        add all elementws (except additionalprops to additionalprops
        add additionalprops optionally to the element
        @param fields: fieldnames to be added normally
        @param kwargs: fields to be added normally or as additional props
        @return: adjustd self.data
        """
        # prepare existing or empty additionalProps dictionary
        additionalprops = dict()
        for name, value in kwargs.items():
            if name in fields:
                self.addoptionalprop(name, value)
            elif name != "additionalProps":
                additionalprops[name] = value
        # add additionalProps back to the structure (only if it is not empty)
        self.addoptionalprop("additionalProps", additionalprops)
        return

    ##### information model
    def modelinfojson(self, modelname, modeltype, mainlanguage,
                      modelversion, **kwargs):
        fields = ["modelname", "modeltype",
                  "mainlanguage", "modelversion",  # mandatory fields
                  "mainlanguage", 'languages',
                  'description', 'targetenvironment',
                  'origintool', 'originref',
                  'datetimecreated', 'additionalProps'
                  ]
        """updates the modelinfo in the already created modelinfo"""
        self.elemtype = "ModelInfo"
        self.data["modelname"] = modelname
        self.data["modeltype"] = modeltype
        self.data["mainlanguage"] = nvl(mainlanguage, "en")
        self.data["modelversion"] = nvl(modelversion, "0.0")
        self.add_restprops(fields=fields,
                           **kwargs)
        return self

    def categoryjson(self, elementid, name, categorytype, **kwargs):
        fields = ["elementid", "name",
                  "categorytype",  # mandatory fields
                  "description",
                  'parent',  # "color",
                  'additionalProps'
                  ]
        self.elemtype = "Category"
        self.data = {"elementid": elementid,
                     "name": name,
                     "categorytype": categorytype
                     }
        self.addoptionalprop(propname="description", value=kwargs.get("descr"))
        self.addoptionalprop(propname="color", value=kwargs.get("color"))
        self.addoptionalprop(propname="parentid", value=kwargs.get("parentid"))
        self.add_restprops(fields=fields,
                           **kwargs)
        return self

    def entityjson(self, elementid, name, **kwargs):
        self.elemtype = "Entity"
        self.data = {"elementid": elementid,
                     "name": name
                     }
        for key, val in kwargs.items():
            self.addoptionalprop(propname=key, value=val)
        return self

    def attributejson(self, elementid, name, domainid, mandatory, parentid, **kwargs):
        self.elemtype = "Attribute"
        self.data = {"elementid": elementid,
                     "name": name,
                     "mandatory": mandatory,
                     "parentid": parentid
                     }
        self.addoptionalprop(propname="domainid",
                             value=self.domainref(domainid=domainid,
                                                  modelname=kwargs.get("domainmodelname"))),
        for key, val in kwargs.items():
            self.addoptionalprop(propname=key, value=val)

        return self

    def keysjson(self, keys: list):
        """ keys are currently a list of list of keyelements,
            which are already passed as parameters"""
        assert False, "should not be used unless structure of keys changes"
        return keys

    def relationendjson(self, assoctext, cardinality, mandatory,
                        entityid=None, tableid=None,
                        historicised=None,
                        arcnumber=None):
        self.elemtype == "RelationEnd"

        if entityid is not None:
            self.data["entityid"] = entityid
        else:
            self.data["tableid"] = tableid

        self.data["assoctext"] = assoctext
        self.data["cardinality"] = cardinality
        self.data["mandatory"] = mandatory
        self.addoptionalprop("historicised", historicised)
        self.addoptionalprop("arcnumber",
                             arcnumber if arcnumber is None else int(arcnumber))

        return self

    def relationjson(self, elementid, relationtype, fwd, bwd, **kwargs):
        self.elemtype = "elem.getadditionalprop('SOURCE-MODEL')"
        self.data = {"elementid": elementid,
                     "relationtype": relationtype
                     }
        self.data["fwd"] = fwd.data if isinstance(fwd, JsonElement) else fwd
        self.data["bwd"] = bwd.data if isinstance(bwd, JsonElement) else bwd

        self.addoptionalprop("examples", kwargs.get("examples"))
        self.addoptionalprop("additionalProps",
                             kwargs.get("additionalProps"))
        return self

    def businessrulejson(self, elementid, restrictedelems: list, **kwargs):
        self.elemtype = "BusinessRule"
        self.data = {"elementid": elementid,
                     "restrictedelements": restrictedelems
                     }

        self.addoptionalprop(propname="description",
                             value=kwargs.get("description")
                             )
        self.addoptionalprop(propname="rule",
                             value=kwargs.get("rule")
                             )
        if kwargs.get("rule") is None and kwargs.get("description") is None:
            # illegal either must be not None, make sure json is still valid
            self.data["rule"] = "??? missing rule ???"

        return self

    def derivationjson(self, derivationtype, targetelement, sourceelement, **kwargs):
        self.elemtype = "Derivation"
        self.data = {"targetelement": targetelement,
                     "sourceelement": sourceelement
                     }
        self.addoptionalprop(propname="derivationtype",
                             value=derivationtype
                             )
        for key, value in kwargs.items():
            self.addoptionalprop(propname=key,
                                 value=value
                                 )

        return self

    def refvaluejson(self, value, **kwargs):
        self.elemtype = "ReferenceValue"
        self.data = {"value": value}
        for key, value in kwargs.items():
            self.addoptionalprop(propname=key,
                                 value=value,
                                 intvalue=key in ()
                                 )
        return self

    def domainref(self, domainid, modelname):
        return domainid if modelname is None \
            else {"domainid": domainid,
                  "modelname": modelname
                  }

    def domainjson(self, elementid, name, **kwargs):
        self.elemtype = "Domain"
        self.data = {"elementid": elementid,
                     "name": name,
                     "domaintype": kwargs.get("domaintype")
                     }
        for key, value in kwargs.items():
            if key == "domaintype": continue
            self.addoptionalprop(propname=key,
                                 value=value,
                                 intvalue=key in ("maxlength", "minlength",
                                                  "minvalue", "maxvalue",
                                                  "fractdigits",
                                                  )
                                 )
        return self

    ##### data models
    def datamodeljson(self, modelname):
        return {"ModelInfo": {"modelname": modelname},
                "Domains": [],
                "Tables": [],
                "Categories": []}

    def dataobjectjson(self, key, name, categoryid, columns, **kwargs):
        self.elemtype == "DataObject"
        self.data = {"elementid": key,
                     "name": name,
                     "categoryid": categoryid,
                     "columns": columns
                     }
        for key, val in kwargs.items():
            self.addoptionalprop(key, val)

        return self

    def columnjson(self, key, name, domainid, mandatory, **kwargs):
        self.elemtype == "Column"
        self.data = {"elementid": key,
                     "name": name,
                     "domainid": self.domainref(domainid=domainid,
                                                modelname=kwargs.get("domainmodelname")),
                     "mandatory": mandatory
                     }
        for key, val in kwargs.items():
            self.addoptionalprop(key, val)

        return self

    ##### Systems
    @staticmethod
    def systemjson(self, elementid, name, **kwargs):
        self.elemtype == "System"
        self.data = {"elementid": elementid,
                     "name": name
                     }
        for key, val in kwargs.items():
            self.addoptionalprop(key, val)
        return self

    ##### Mapping
    def mappingjson(self, targetelement, sourceelement, **kwargs):
        self.elemtype == "Mapping"
        self.data = {"targetelement": targetelement,
                     "sourceelement": sourceelement
                     }
        for key, value in kwargs.items():
            self.addoptionalprop(propname=key,
                                 value=value
                                 )

        return self
