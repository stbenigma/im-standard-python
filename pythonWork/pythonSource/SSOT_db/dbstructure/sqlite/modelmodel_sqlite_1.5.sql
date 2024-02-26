-- Upgrade db to version 1.5
-- add unique key with NULL to 2 unique keys without
create table tabl_enti_maps_tmp
(
	tema_id integer
		primary key autoincrement,
	tema_tabl_id integer not null
		references tables
			on delete cascade,
	tema_enti_id integer
		constraint tema_enti_fk
			references ENTITIES (enti_id)
				on delete cascade,
	tema_rela_id integer
		constraint tema_rela_fk
			references RELATIONS (rela_id)
				on delete cascade,
	constraint tema_unenti
		unique (tema_tabl_id, tema_enti_id),
	constraint tema_unrela
		unique (tema_tabl_id, tema_rela_id),
	constraint tema_ck
		check ((tema_enti_id is not null and tema_rela_id is null )
      	        		  or (tema_enti_id is null and tema_rela_id is not null))
);
insert into tabl_enti_maps_tmp (tema_tabl_id,tema_enti_id,tema_rela_id) select distinct tema_tabl_id,tema_enti_id,tema_rela_id from tabl_enti_maps;
drop table tabl_enti_maps;
alter table tabl_enti_maps_tmp rename to tabl_enti_maps;
-- END alter unique key

-- change to mode-id-reference add unique key with NULL to 2 unique keys without
create table businessrule_elements_tmp
    (
     bure_id integer not null primary key autoincrement,
     bure_buru_id numeric (10) not null ,
     bure_mode_id numeric (10) not null ,
     bure_writeable varchar (5) not null constraint ck__businessr__bure___10216507 check ( bure_writeable='TRUE' or bure_writeable='FALSE' ) ,
     bure_uc varchar (30) not null ,
     bure_dc datetime (8) not null ,
     bure_um varchar (30) null ,
     bure_dm datetime (8) null ,
 	constraint bure_uk
 		unique (bure_buru_id,bure_mode_id),
	constraint bure_mode_fk foreign key (bure_mode_id)
    references modelelement (mode_id)
);

insert into businessrule_elements_tmp (bure_id, bure_buru_id, bure_mode_id, bure_writeable, bure_uc, bure_dc , bure_um, bure_dm) 
		select bure_id, bure_buru_id, bure_mode_id, bure_writeable, bure_uc, bure_dc , bure_um, bure_dm from businessrule_elements;
drop table businessrule_elements;
alter table businessrule_elements_tmp rename to businessrule_elements;
-- END alter unique key

-- new table
create table examples 
    (
     expl_id integer (10) not null primary key
		references modelelement (mode_id)
		on delete cascade,
     expl_value varchar (4000) not null , 
     expl_enti_id numeric (10) , 
     expl_attr_id numeric (10) , 
     expl_uc varchar (30) not null , 
     expl_dc varchar(30) not null , 
     expl_um varchar (30) , 
     expl_dm varchar(30)
	 ,constraint fkarc_8 check ( 
	 	        (  (expl_enti_id is not null) and 
	 	         (expl_attr_id is null) ) or 
	 	        (  (expl_attr_id is not null) and 
	 	         (expl_enti_id is null) )  
			 )
	,constraint expl_enti_uk unique  (expl_value, expl_enti_id)
	,constraint expl_attr_uk unique  (expl_value, expl_attr_id)
	,constraint expl_attr_fk foreign key (expl_attr_id) 
		references attributes (attr_id ) 
		on delete cascade
	,constraint expl_enti_fk foreign key ( expl_enti_id) 
		references entities (enti_id ) 
		on delete cascade
    );
-- end new table

INSERT INTO modelelem_type (melt_id, melt_shortname, melt_name, melt_uc, melt_dc) VALUES (23, 'EXPL', 'Example', 'SYS', '2023-12-29');

-- add type to modelelement_type
create table modelelem_type_tmp
(
	melt_id integer not null
		primary key autoincrement,
	melt_shortname varchar(4) not null
		constraint melt_un
			unique,
	melt_name varchar(60) not null
		constraint melt_un2
			unique,
	melt_uc varchar(30),
	melt_dc varchar(30) not null,
	melt_um varchar(30),
	melt_dm varchar(30),
	check (melt_shortname in ('ARCS', 'ATTR', 'BURU', 'COLU', 'DOMA', 'ENTI'
                                , 'INTF', 'ORGU', 'RELA', 'SYNO', 'TABL','DOCU','KEYS','DATY'
                                ,'DGRM','DIAG','EXPL'))
);
insert into modelelem_type_tmp select * from modelelem_type;
drop table modelelem_type;
alter table modelelem_type_tmp rename to modelelem_type;
INSERT INTO modelelem_type (melt_id, melt_shortname, melt_name, melt_uc, melt_dc) VALUES (17, 'EXPL', 'Example', 'SYS', '2023-12-29');
commit;


create table modelelement_tmp
(
	mode_id integer not null
		primary key autoincrement,
	mode_type varchar(4) not null,
	mode_melt_id integer not null
		references modelelem_type (melt_id),
    mode_min_zoom_level numeric(1) null check ( mode_min_zoom_level between 0 and 4 ) ,
    mode_max_zoom_level numeric(1)  null check ( mode_max_zoom_level between 0 and 4 ) ,
    mode_dev_status varchar (4) null default "DEV" check ( mode_dev_status in ("DEV", "REL", "TEST") ),
	check (mode_type in ("ARCS", "ATTR", "BURU", "COLU", "DOMA", "ENTI"
                            , "INTF", "ORGU", "RELA", "SYNO", "TABL","DOCU"
							,"KEYS","DATY","DGRM","DIAG","EXPL"))
);
insert into modelelement_tmp select from modelelement;
drop table modelelement;
alter table modelelement_tmp rename to modelelement_tmp;
-- end add Type


-- add unique to buru
CREATE UNIQUE INDEX buru_un ON business_rules(buru_name);

drop view dbversion;
create view dbversion as select '1.5' as version, datetime() as installedtime;
