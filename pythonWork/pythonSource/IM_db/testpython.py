
from IM_OBJECTS import *
from IM_DB import parameters,dbConnect,dbDDL,dbDML,dbErstelleTables,dbInserts,dbLookup,dbParam
import sys,re


if (__name__ == '__main__'):
    parameters.initparam(p_callarg=sys.argv[1])
    dbConnect.openDB(p_filepath= parameters.dbFilePath());

    #    print(re.findall(r',\s*[a-z0-9_]+',
    #print (re.findall(r'CREATE\s+TABLE\s+[a-z$0-9_]+\s*\(\s*([a-z$0-9_]+)'
#    print(re.findall(r',\s*([a-z$0-9_]+)'
#    print(re.findall(r',\s*([a-z$0-9_]+)'
#    print(re.match(r'CREATE\s+TABLE\s+[a-z$0-9_]+\s*\(\s*([a-z$0-9_]+)(,\s*([a-z$0-9_]+)[^,]+)*]'
#    print(re.findall(r'CREATE\s+TABLE\s+[a-z$0-9_]+\s*\(\s*([a-z$0-9_]+)'
    print(re.findall(r',\s*([a-z$0-9_]+)[^,]+'
                     ,"""CREATE TABLE tabellen
        (
         TABL_ID integer primary key autoincrement , 
         TABL_NAME VARCHAR (60) NOT NULL , 
         TABL_SCHN_ID integer NOT NULL , 
         TABL_PREFIX VARCHAR (60) NULL , 
         TABL_BESCHR VARCHAR (4000) NULL , 
     	 TABL_odm_guid	varchar(36),
         TABL_UC VARCHAR (30) NOT NULL , 
         TABL_DC VARCHAR (30) NOT NULL , 
         TABL_UM VARCHAR (30) NULL , 
         TABL_DM VARCHAR (30) NULL ,
    	  CONSTRAINT TABL_UN UNIQUE (TABL_SCHN_ID , TABL_NAME)
     	   ,CONSTRAINT TABL_SCHN_FK FOREIGN KEY (TABL_SCHN_ID) 
     	      REFERENCES SCHNITTSTELLE (SCHN_ID ) 
        )""",re.IGNORECASE))

#    ss = Sprache.select()
#    s = Sprache()
#    ss = Tabelle.indexlist()
#    t = Tabelle().getbyid(302)
#    print(t.__dict__)
#    print (Tabelle.mappingto(302))
#    for s in ss:
#        print (s)
#    print (baseobject.webanker(Tabelle,302).__dict__)

