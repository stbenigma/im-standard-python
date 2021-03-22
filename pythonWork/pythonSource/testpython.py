from IM_DB import dbDML
def t (**colvals):
      print (colvals)
      print(dbDML.valuepairs2sqlexpr(**colvals))

t(col1='axx',col2=None,col3=123)
