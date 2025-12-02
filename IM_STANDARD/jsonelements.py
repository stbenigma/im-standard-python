from IM_STANDARD import nvl

class JsonElements:

    """ all functions to create standard json structures"""

    def __init__(self):
        """ only static functions, no instance code"""
        return

    ##### General functions
    @staticmethod
    def optionalprop(destobject, propname, value, intvalue=None):
        """sets a value into a json structure as propname if
           the value is not empty (None, "", [], {})
           if intvalue: value is set as integer, not as string
          """
        if not (value is None or value == "" or \
                (type(value) in (list, dict) and len(value) == 0)):
            # property is only set, if it is not null or not empty
            if type(destobject) == dict:
                destobject[propname] = int(float(value)) if intvalue else value
            elif type(destobject)== list:
                destobject.append({propname: int(float(value)) if intvalue else value})
            else:
                raise Exception(f"unkown type to add property {type(destobject)}")
        return

    @staticmethod
    def getadditionalprop(elem,name):
        adprop=elem.get("additionalProps",[])
        if len(adprop) ==0:
            return None
        prop=[p.get(name) for p in adprop if name in p]
        assert len(prop)<2,f"property {name} found twice {prop}"
        if len(prop)==0:
            return None
        else:
            return prop[0]

    @staticmethod
    def additionalprops(props):
        """
        @param props: dictionary with properties to be collected as additional properties
        @return: dictionary with all properties which are not empty (None, "", [], {}
                None if props is None
        """
        if props is None:
            retval = None
        else:
            retval = dict()
            for key, val in props.items():
                JsonElements.optionalprop(destobject=retval,
                                        propname=key,
                                        value=val
                                        )
        return retval

    def add_restprops(self, jsonstruct, fields, **kwargs):
        """
        add all values of kwargs beeing in fields to the jsonstruct (as optional elements).
        add all elementws (except additionalprops to additionalprops
        add additionalprops optionally to jsonstruct
        @param jsonstruct: structure to fill
        @param fields: fieldnames to be added normally
        @param kwargs: fields to be added normally or as additional props
        @return: adjustd jsonstruct
        """
        # prepare existing or empty additionalProps dictionary
        additionalprops = list()
        for name, value in kwargs.items():
            if name in fields:
                self.optionalprop(jsonstruct, name, value)
            elif name != "additionalProps":
                additionalprops.append({name: value})
        # add additionalProps back to the structure (only if it is not empty)
        self.optionalprop(jsonstruct, "additionalProps", additionalprops)
        return

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
        jsonstruct = self.jsonschemamodel["ModelInfo"]
        jsonstruct["modelname"] = modelname
        jsonstruct["modeltype"] = modeltype
        jsonstruct["mainlanguage"] = nvl(mainlanguage, "en")
        jsonstruct["modelversion"] = nvl(modelversion, "0.0")
        self.add_restprops(jsonstruct=jsonstruct,
                           fields=fields,
                           **kwargs)
        # additionalprops=nvl(kwargs.get("additionalProps"),dict())
        # for name, value in kwargs.items():
        #    if name in fields:
        #        self.optionalprop(jsonstruct, name, value)
        ##    elif name != "additionalProps":
        #        additionalprops[name]=value
        # self.optionalprop(jsonstruct, "additionalProps", additionalprops)
        return jsonstruct

    def categoryjson(self, elementid, name, categorytype, **kwargs):
        fields = ["elementid", "name",
                  "categorytype",  # mandatory fields
                  "description",
                  'parent',  # "color",
                  'additionalProps'
                  ]
        jsonstruct = {"elementid": elementid,
                      "name": name,
                      "categorytype": categorytype
                      }
        self.optionalprop(jsonstruct, "description", kwargs.get("descr"))
        self.optionalprop(jsonstruct, "color", kwargs.get("color"))
        self.optionalprop(jsonstruct, "parent", kwargs.get("parent"))
        # self.optionalprop(jsonstruct, "additionalProps", kwargs.get("additionalProps"))
        self.add_restprops(jsonstruct=jsonstruct,
                           fields=fields,
                           **kwargs)
        return jsonstruct


    ##### information model
    def entityjson(self, elementid, name,  **kwargs):
        jsonstruct = {"elementid": elementid,
                      "name": name
                      }
        for key, val in kwargs.items():
            self.optionalprop(jsonstruct, key, val)
        return jsonstruct


    def attributejson(self, elementid, name, domainid, mandatory, parentid, **kwargs):
        jsonstruct = {"elementid": elementid,
                      "name": name,
                      "mandatory": mandatory,
                      "parentid": parentid
                      }
        self.optionalprop(jsonstruct, "domainid",
                          self.domainref(domainid=domainid,
                                 modelname=kwargs.get("domainmodelname"))),
        for key, val in kwargs.items():
            self.optionalprop(jsonstruct, key, val)

        return jsonstruct

    def keysjson(self, keys: list):
        """ keys are currently a list of list of keyelements,
            which are already passed as parameters"""
        return keys

    def relationendjson(self, assoctext, cardinality, mandatory,
                        entityid=None, tableid=None,
                        historicised=None,
                        arcnumber=None):
        jsonstruct = dict()
        if entityid is not None:
            jsonstruct["entityid"] = entityid
        else:
            jsonstruct["tableid"] = tableid

        jsonstruct["assoctext"] = assoctext
        jsonstruct["cardinality"] = cardinality
        jsonstruct["mandatory"] = mandatory
        self.optionalprop(jsonstruct, "historicised", historicised)
        self.optionalprop(jsonstruct, "arcnumber", arcnumber if arcnumber is None else int(arcnumber))

        return jsonstruct

    def relationjson(self, elementid, relationtype, fwd, bwd, **kwargs):
        jsonstruct = {"elementid": elementid,
                      "relationtype": relationtype
                      }
        jsonstruct["fwd"] = fwd
        jsonstruct["bwd"] = bwd

        self.optionalprop(jsonstruct, "examples", kwargs.get("examples"))
        self.optionalprop(jsonstruct, "additionalProps",
                          kwargs.get("additionalProps"))
        return jsonstruct

    def businessrulejson(self, elementid, restrictedelems: list, **kwargs):
        jsonstruct = {"elementid": elementid,
                      "restrictedelements": restrictedelems
                      }

        self.optionalprop(destobject=jsonstruct,
                          propname="description",
                          value=kwargs.get("description")
                          )
        self.optionalprop(destobject=jsonstruct,
                          propname="rule",
                          value=kwargs.get("rule")
                          )
        if kwargs.get("rule") is None and kwargs.get("description") is None:
            # illegal either must be not None, make sure json is still valid
            jsonstruct["rule"] = "??? missing rule ???"

        return jsonstruct

    def derivationjson(self, derivationtype,sourceelementname, **kwargs):
        jsonstruct = {"derivationtype": derivationtype,
                      "sourceelementname": sourceelementname
                      }
        for key, value in kwargs.items():
            self.optionalprop(destobject=jsonstruct,
                              propname=key,
                              value=value
                              )


        return jsonstruct


    def refvaluejson(self, value, **kwargs):
        jsonstruct = {"value": value}
        for key, value in kwargs.items():
            self.optionalprop(destobject=jsonstruct,
                              propname=key,
                              value=value,
                              intvalue=key in ()
                              )
        return jsonstruct

    def domainref(self, domainid, modelname):
        return domainid if modelname is None \
            else {"domainid": domainid,
                  "modelname": modelname
                  }

    def domainjson(self, elementid, name, **kwargs):
        jsonstruct = {"elementid": elementid,
                      "name": name,
                      "domaintype": kwargs["domaintype"]
                      }
        for key, value in kwargs.items():
            if key == "domaintype": continue
            self.optionalprop(destobject=jsonstruct,
                              propname=key,
                              value=value,
                              intvalue=key in ("maxlength", "minlength",
                                               "minvalue", "maxvalue",
                                               "fractdigits",
                                               )
                              )
        return jsonstruct
    ##### data models
    def datamodeljson(self, modelname):
        return {"ModelInfo": {"modelname": modelname},
                "Domains": [],
                "Tables": [],
                "Categories": []}

    def dataobjectjson(self, key, name, categoryid, columns, **kwargs):
        jsonstruct = {"elementid": key,
                      "name": name,
                      "categoryid": categoryid,
                      "columns": columns
                      }
        for key, val in kwargs.items():
            self.optionalprop(jsonstruct, key, val)

        return jsonstruct

    def columnjson(self, key, name, domainid, mandatory, **kwargs):
        jsonstruct = {"elementid": key,
                      "name": name,
                      "domainid": self.domainref(domainid=domainid,
                                          modelname=kwargs.get("domainmodelname")),
                      "mandatory": mandatory
                      }
        for key, val in kwargs.items():
            self.optionalprop(jsonstruct, key, val)

        return jsonstruct

    ##### Systems
    @staticmethod
    def systemjson(self, elementid, name, **kwargs):
        jsonstruct = {"elementid": elementid,
                      "name": name
                      }
        for key, val in kwargs.items():
            self.optionalprop(jsonstruct, key, val)
        return jsonstruct

    ##### Mapping
    @staticmethod
    def mappingjson(self, name, **kwargs):
        jsonstruct = {"name": name}
        for key, val in kwargs.items():
            self.optionalprop(jsonstruct, key, val)

        return jsonstruct




