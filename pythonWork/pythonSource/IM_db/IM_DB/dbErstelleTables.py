# -*- coding: latin-1 -*-
from IM_DB import *
from IM_OBJECTS import *

def erstelleInfra():
    #erlaube alles droppen
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

    dbDDL.dropTable("geschaeftsbereich");
    dbDDL.createTable("""CREATE TABLE geschaeftsbereich 
				      (
				      gber_id              integer primary key autoincrement,
				      gber_name            VARCHAR(60)NOT NULL,
				      gber_beschreibung   VARCHAR(4000)NULL,
				      gber_zweck           VARCHAR(2000)NULL,
				      gber_uc  VARCHAR(30) not null , 
				       GBER_DC VARCHAR(30)  NOT NULL , 
				       GBER_UM VARCHAR (30),
				      gber_dm VARCHAR(30),
				      CONSTRAINT Bereich_UN UNIQUE (gber_name asc)
				  )""")
    dbDDL.dropTable("bereich_elemdarst");
    dbDDL.createTable("""CREATE TABLE bereich_elemdarst 
				      ( beld_id integer primary key autoincrement,
				       BELD_MELT_ID INTEGER NOT NULL , 
				       BELD_GBER_ID INTEGER NOT NULL , 
				       BELD_BREITE INTEGER NULL , 
				       BELD_HOEHE INTEGER NULL , 
				       BELD_DECKKRAFT INTEGER NULL DEFAULT 100 CHECK ( BELD_DECKKRAFT BETWEEN 0 AND 100 ) , 
				       BELD_FARBE VARCHAR (6) NULL DEFAULT '000000' CHECK ( LENGTH(BELD_FARBE) = 6 ) , 
				       BELD_RANDBREITE INTEGER NULL DEFAULT 1 , 
				       BELD_RANDDECKKRAFT INTEGER NULL DEFAULT 100 CHECK ( BELD_RANDDECKKRAFT BETWEEN 0 AND 100 ) , 
				       BELD_RANDFARBE VARCHAR (6) NULL DEFAULT '000000' CHECK ( LENGTH(BELD_RANDFARBE) = 6 ) , 
				       BELD_SCHRIFTGROESSE INTEGER NULL CHECK ( BELD_SCHRIFTGROESSE BETWEEN 1 AND 999 ) , 
				       BELD_SCHRIFTFARBE VARCHAR (6) NULL DEFAULT '000000' CHECK ( LENGTH(BELD_SCHRIFTFARBE) = 6 ) , 
				      BELD_UC VARCHAR (30) NULL , 
				       BELD_DC VARCHAR (30) NOT NULL , 
				       BELD_UM VARCHAR (30) NULL , 
				       BELD_DM VARCHAR (30) NULL ,
				      CONSTRAINT BELD_UN UNIQUE (beld_melt_id,beld_gber_id),
					  CONSTRAINT beld_mode_fk FOREIGN KEY(beld_melt_id)
					          REFERENCES modellelem_typ(melt_id)
					              ON DELETE CASCADE ,
					  CONSTRAINT beld_gber_fk FOREIGN KEY(beld_gber_id)
	  				          REFERENCES geschaeftsbereich(gber_id)
	  				              ON DELETE CASCADE 
			      )""")

    Document.createtable()
    ModelelemDocu.createtable()
    OragnisationalUnit.createtable()
    ModelelemOrgu.createtable()
    TablEntiMap.createtable()
    AttrTransf.createtable()
    Entity.createviews()
#end erstelleInfra