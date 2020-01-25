
//div. scripts to change tables after generation
function names2sqlcompatible(){
	// removes all non-sql-compatible characters from
	// all names
 var tables = model.getTableSet().toArray();
 for (var t = 0; t<tables.length;t++){
	table = tables[t];
	tabname = table.getName().replace("-","_");
	table.setName(tabname.toUpperCase());

 	columns = table.getElements();
     for (var i = 0; i < columns.length; i++) {
        column = columns[i];
        colname = column.getName().replace("-","_");
        column.setName(colname.toUpperCase());
 
 	keys = table.getKeys();
 	for (var i = 0; i < keys.length; i++) {
  		key = keys[i];
    		if(!key.isFK()){
     		kname = key.getName().replace("-","_");
     		key.setName(kname.toUpperCase());
   		}else{
	     	kname = key.getFKAssociation().getName().replace("-","_");
     		key.getFKAssociation().setName(kname.toUpperCase());
     		key.getFKAssociation().setDirty(true);
   		}
 	table.setDirty(true);
 }
} 

fumction gettempaltetable(){
 templtable = model.getTableSet().getById(model.getTemplateTableID())
 return templtable
}

function tablecolprefix(table) {
	return table.getAbbreviation().toCpperCase() + "_";
}

function 	columnprefix1table(table) {
 // sets the column Prefix to table abbrev for 1 table
 	abbr = tablecolprefix(table);
 	if(!"_".equals(abbr)){
     columns = table.getElements();
     for (var i = 0; i < columns.length; i++) {
        column = columns[i];
        cname = column.getName().toUpperCase;
        if(!cname.startsWith(abbr)){
        	column.setName(abbr+cname);
        }
     }
}

function columnprefix() {
 var temptable = gettemplatetable();
 var tables = model.getTableSet().toArray();
 for (var t = 0; t<tables.length;t++){
 	if(!table.getId() == templtable.getId()) {
	 	table = tables[t];
 		columnprefix1table(table)
     	table.setDirty(true)
 	}	 
 }
}

function addtemplatecols() {
 // columns are found by column name or ABBREV_colname
//prop var colproptemplcolid = "coltemplID";
 var templtable =  gettempaltetable();
 if(template!=null){
    tcolumns = template.getElements();
    tables = model.getTableSet().toArray();
    for (var t = 0; t<tables.length;t++){
     table = tables[t];
     // compare id to exclude templ table
     if(!table.getId() == templtable.getId()) {
         for (var i = 0; i < tcolumns.length; i++) {
	     	column = tcolumns[i];
            col = table.getElementByName(column.getName());
            if(col==null){
			// evtl. schon mit prefix vorhanden
              col = table.getElementByName(tablecolprefix(table) + column.getName());
            }
//prop            if(col==null){
//prop             col = table.getColumnByProperty(colproptemplcolid,column.getObjectID());
//prop            }
            if(col==null){
             col = table.createColumn();
            }
            column.copy(col);
            //set property after copy otherwise it will be cleared by copy
//prop            col.setProperty(colproptemplcolid,column.getObjectID());
 	   	    columnprefix1table(table)
            table.setDirty(true);
         }
     }
 }
}

function alltables(){
	// does all changes to all tables
	names2sqlcompatible;
	columnprefix();
	addtemplatecols();
}

