
// div. functions to handle complex logical manipulations
function subviewfromsearch() {
objs = model.getLastSearchResult().toArray();
var dp;
var sv;
//create subview and add tables to it
for(var i = 0;i<objs.length;i++){
	obj = objs[i];
	// use "Entity" for entities and logical model
	if(obj.getObjectTypeName().equals("Table")){
		if(dp==null){
			dp = obj.getDesignPart();
			sv = dp.createDesignPartSubView();
			// uncomment next line if want to set name
		     //sv.setName("Name");
		     sv.getPlaceHolder().setVisible(true);
		}
		sv.addViewFor(obj);
	}
}
if(dp!=null){
 //add foreign keys if you want to
 for(var i = 0;i<objs.length;i++){
	obj = objs[i];
	// use "Entity" for entities and logical model
	if(obj.getObjectTypeName().equals("Table")){
		tv = obj.getFirstViewForDPV(sv);
		if(tv!=null){
			//for entities and logical model use 
			//tv.addTVRelations(); 
			tv.addTVFKRelations();
		}
	}
 }
 //add Arcs if you want to
 for(var i = 0;i<objs.length;i++){
	obj = objs[i];
	if(obj.getObjectTypeName().equals("Table")){
		tv = obj.getFirstViewForDPV(sv);
		if(tv!=null){
			tv.addArcs();
		}
	}
 }
 //arrange diagram
 sv.rearrangeNewDiagram();
}
}
