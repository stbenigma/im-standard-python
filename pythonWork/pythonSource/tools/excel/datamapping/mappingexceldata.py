WS_OVERVIEW = "Overview"
WS_ENT2TABMAP = "Entity to Table mapping"
WS_TAB2ENTMAP = "Table to Entity mapping"
WS_ATTR2COLMAP = "Attributes to Columns mapping"
WS_COL2ATTRMAP = "Columns to Attributes mapping"
WS_OVERVIEWSHEETS = [WS_OVERVIEW,  # overview must be the first one!
                     WS_ENT2TABMAP,
                     WS_TAB2ENTMAP,
                     WS_ATTR2COLMAP
                     ]

IMHEAD = "Information Model"
IMHEADERS = ['entityName', 'attrName']
COLHEADERS = ['tableName', 'tableCRUD', 'columnName', 'columnRW',
              'column-ID', 'domain', 'dataType',
              'mand.', 'default value', 'descr', 'rules']
COLMAPHEADERS = [COLHEADERS[0]] + COLHEADERS[2:5]
#MINMAPHEADERS = [COLHEADERS[0], COLHEADERS[2]] + IMHEADERS

# map headers to js-lables fill with attrlists, amend individually
attrmatchkey2js = {v: {"colidx":idx,"jskey":v} for idx,v in enumerate(COLHEADERS + IMHEADERS,start=1)}
# attrmatchkey2js['tableName'] = "json label-equivalent"

attrmatchjs2key = {val["jskey"]: key for key, val in attrmatchkey2js.items()}

def attrkey2js(s):
    return None if s not in attrmatchkey2js else attrmatchkey2js[s]

def attrkey2idx(s):
    return None if s not in attrmatchkey2js else attrmatchkey2js[s]['colidx']

def attrjs2key(s):
    return None if s not in attrmatchjs2key else attrmatchjs2key[s]


