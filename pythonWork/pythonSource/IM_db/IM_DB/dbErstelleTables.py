# -*- coding: latin-1 -*-
from IM_DB import dbDDL
from pathlib import Path

def erstelleInfra(psqlfilename):
    sqltxt = Path(psqlfilename).read_text()
    dbDDL.execscript(psql=sqltxt)
    return

    """ old solution without file and statements in every object
    PhysicalUnit.createtable()
    Storageformat.createtable()
    Interface.createtable()
    Table.createtable()
    Column.createtable()
    Datatype.createtable()

    Entity.createtable()
    Synonym.createtable()

    Key.createtable()
    Keyelement.createtable()

    Domain.createtable()
    DomaingroupMember.createtable()
    DefaultValue.createtable()

    Attribute.createtable()

    Arc.createtable()

    Relation.createtable()

    Modelelemtype.createtable()
    Modelelement.createtable()
    Externalref.createtable()
    ModelelementProperty.createtable()

    Language.createtable()
    Languagetext.createtable()

    Diagramtype.createtable()
    Diagram.createtable();

    MeltDiat.createtable();

    Elementrep.createtable()
    Relationrep.createtable()
    Linesegment.createtable()

    Userdefprop.createtable()
    Userdefpropvalue.createtable()
    Project.createtable()

    Document.createtable()
    ModelelemDocu.createtable()
    OragnisationalUnit.createtable()
    ModelelemOrgu.createtable()
    TablEntiMap.createtable()
    ColAttrMap.createtable()
    Entity.createviews()
    """
#end erstelleInfra