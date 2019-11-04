	<lib id="3648E159-EDD2-ECD1-C014-A11CB3E804A5" name="translation" engine="Oracle Nashorn" methods="initTranslation,change2DE,change2EN" >
		<script>
			<![CDATA[
//scripts to handle translation of model
var gLogNote = "LOG";
var gCurrentLang = "DE";
var gLanguages = "DE,EN";
var gTranslInforegexp =/TRANSLATION\{[^}]*\}/;
var logInitialized = false;
var notesStartTag = '[<tag>[\n';
var notesEndTag = '\n]<tag>]';

function initLog(){
	if (! logInitialized){
		var lNote = model.getNoteSet().getByName(gLogNote);
     	if (lNote == null) {
    	    		lNote = model.createNote()
	    		lNote.setName(gLogNote);
     	}
     	lNote.setComment("");
     	logInitialized = true;
	}
}
function log(plog){
	initLog();
	var lNote = model.getNoteSet().getByName(gLogNote);
     lNote.setComment(lNote.getComment()+"\n"+plog);
}

function getTranslInfo(){
	var lDesignComment = model.design.getComment();
     lmatchTransl= lDesignComment.match(gTranslInforegexp);
     return lmatchTransl;    
}

function setTranslInfo(curLang,langs) {
	model.design.setComment(
		"TRANSLATION{\ncurrentLang="
		+curLang+"\nlanguages="
		+langs+"\nlastSync=\n}\n"
		+ model.design.getComment());
}
function updTranslInfo(curLang,langs,datetime) {
	curComment = model.design.getComment();
	model.design.setComment(
		curComment.replace(gTranslInforegexp,
		"TRANSLATION{\ncurrentLang="
		+curLang+"\nlanguages="
		+langs+"\nlastSync="+datetime+"\n}"
		));
}

function buildRegExpTag(innertag,tag){
	return tag.replace('<tag>',innertag).replace(/\[/g,'\\[').replace(/\]/g,'\\]')
}

function textFromNote(tag,obj) {
    	note = obj.getNotes()
    	restart =  buildRegExpTag(tag, notesStartTag)
    	reend =  buildRegExpTag (tag, notesEndTag)
    	//throw new Error (restart+"*"+reend);
    	re = new RegExp(restart + '([^]*)' + reend)
    	ma = note.match(re)
    	retval = ''
   	if (ma != null) {
   		retval = ma[1]
	}
	return retval
}

function textToNote(tag,obj,value) {
    	note = obj.getNotes()
    	restart =  buildRegExpTag(tag, notesStartTag)
    	reend =  buildRegExpTag (tag, notesEndTag)
    	re = new RegExp(restart + '([^]*)' + reend)
    	ma = note.match(re)
    	newentry = notesStartTag.replace('<tag>',tag) 
    			+ value 
    			+ notesEndTag.replace('<tag>',tag)
    			+ "\n"
   	if (ma == null) {
   		note = note + newentry
	} else {
		note = note.replace(re , newentry)
	}

	obj.setNotes(note)
}

function init(){
	lmatchTransl = getTranslInfo();
	if (lmatchTransl == null) {
		throw new Error("***TRANSLATION not installed***");
	}
	ltext= String(lmatchTransl).match(/currentLang=[A-Z]{2}/);
	lparts = String(ltext).split("=");
	//log("curLang="+lparts[1]);
     gCurrentLang = lparts[1];

	ltext= String(lmatchTransl).match(/languages=[A-Z,]*/);
	lparts = String(ltext).split("=");
     //log("languages="+lparts[1]);
     gLanguages = lparts[1]
}

function doProperty(lang,propName,obj,value){
	lpropName = lang + propName;
	if (lang == gCurrentLang) {
		// die Werte kommen aus dem Objekt, überschreibe immer
		obj.setProperty(lpropName
		      	 	,value)
	} else {
	   	ldest = obj.getProperty(lpropName);
	   	// überschreibe nur, wenn das Ziel leer ist
		if (ldest == '')  {
		 	// bei leerem sourceWert setze keinen Prefix
			if (value != '') {
				lprefix =  '*'+gCurrentLang+'* '
				obj.setProperty(lpropName,lprefix+value)
			} 
			
		}
	}
}

function doNote(lang,tag,obj,value) {
	if (lang == gCurrentLang) {
		// die Werte kommen aus dem Objekt, überschreibe immer
		textToNote(lang+tag,obj,value)
	} else {
	   	ldest = textFromNote(lang+tag,obj);
	   	// überschreibe nur, wenn das Ziel leer ist
		if (ldest == '')  {
		 	// bei leerem sourceWert setze keinen Prefix
			if (value != '') {
				lprefix =  '*'+gCurrentLang+'* '
				textToNote(lang+tag,obj,lprefix+value)
			} 
			
		}
	}
	
}			
	
function fuellUDP(){
	entities = model.getEntitySet().toArray();
	for (i=0;i<entities.length;i++) { //
		ent = entities[i];
		// noch nicht initialisiert
		langs = gLanguages.split(',');
		for (i=0;i<langs.length;i++) {
			doProperty(langs[i],"_ENTI_NAME",ent,ent.getName())
//			doProperty(langs[i],"_ENTI_COMMENT",ent,ent.getComment())
			doNote(langs[i],"DE_ENTI_COMMENT",ent,ent.getComment())
			doProperty(langs[i],"_ENTI_SYNONYM",ent,ent.getSynonym())
		}
	
		attrs = ent.getAttributes().toArray();
		//log("Attrs="+attrs.length)
		for (j=0;j<attrs.length;j++) { //
			attr = attrs[j];
			//log(attr.getName(),attr.getComment());
			for (i=0;i<langs.length;i++) {
				doProperty(langs[i],"_ATTR_NAME",attr,attr.getName());
//				doProperty(langs[i],"_ATTR_COMMENT",attr,attr.getComment());			
				doNote(langs[i],"_ATTR_COMMENT",attr,attr.getComment());			
		}
		}
		ent.setDirty(true);
	}
	relationships = model.getRelationSet().toArray();
	for (r=0;r<relationships.length;r++) { //
		rel = relationships[r];
		sourcename = rel.getNameOnSource()
		targetname = rel.getNameOnTarget()
		langs = gLanguages.split(',');
		for (i=0;i<langs.length;i++) {
			//if (i > 0) throw new Error ("\n"+langs[i]+"_RELA_TEXT_FROM"+"\n"+langs.length);
			doProperty(langs[i],"_RELA_TEXT_FROM",rel,sourcename)
			doProperty(langs[i],"_RELA_TEXT_TO",rel,targetname)	
		}
		rel.setDirty(true);
	}
}

function setProperties(lang){
	entities = model.getEntitySet().toArray();
	for (i=0;i<entities.length;i++) { //
		ent = entities[i];
		ent.setName(ent.getProperty(lang+"_ENTI_NAME"));
//		ent.setComment(ent.getProperty(lang+"_ENTI_COMMENT"));
		ent.setComment(textFromNote(lang+"_ENTI_COMMENT",ent))
		ent.setSynonym(ent.getProperty(lang+"_ENTI_SYNONYM"));
		
		attrs = ent.getAttributes().toArray();
		//log("Attrs="+attrs.length)
		for (j=0;j<attrs.length;j++) { //
			attr = attrs[j];
			//log(attr.getName(),attr.getComment());
			attr.setName(attr.getProperty(lang+"_ATTR_NAME"));
//			attr.setComment(attr.getProperty(lang+"_ATTR_COMMENT"));			
			attr.setComment(textFromNote(lang+"_ATTR_COMMENT",attr))
		}		
		ent.setDirty(true);
	}
	relationships = model.getRelationSet().toArray();
	for (r=0;r<relationships.length;r++) { 
		rel = relationships[r];
		rel.setNameOnSource(rel.getProperty(lang+"_RELA_TEXT_FROM"));
		rel.setNameOnTarget(rel.getProperty(lang+"_RELA_TEXT_TO"));
		rel.setDirty(true);
	}
}

function curDateStr(){
	var currentdate = new Date();
	return  currentdate.getDate() 
	+ "/" + (currentdate.getMonth()+1) 
	+ "/" + currentdate.getFullYear() + "  " 
	+ currentdate.getHours() + ":" 
	+ currentdate.getMinutes() + ":" + currentdate.getSeconds();
}
function initTranslation() {
	lmatchTransl= getTranslInfo()
	if (lmatchTransl == null) {
		setTranslInfo(gCurrentLang
		,gLanguages);		
	} else {
		throw new Error("***TRANSLATION already installed***");
	}
	//hier gibt es einen Eintrag für die Translation
	init();
	// fülle die UDP für die Übersetzungen
	fuellUDP();
	updTranslInfo(gCurrentLang, gLanguages
				,curDateStr());
	model.design.setDirty(true);
}


function changeLang(pfromLang,ptoLang){
	//log("3:"+gLanguages);
//	log("change from " + pfromLang + " to " + ptoLang);
	fuellUDP();
	setProperties(ptoLang);
	gCurrentLang = ptoLang;
	updTranslInfo(gCurrentLang, gLanguages
				,curDateStr());	
	model.design.setDirty(true);
}

function change2DE() {
	init();
	if (gCurrentLang != 'DE') {
		changeLang(gCurrentLang,'DE');
	}
}
	
function change2EN() {
	init();
	if (gCurrentLang != 'EN') {
		changeLang(gCurrentLang,'EN');
	}
}
]]>
		</script>
