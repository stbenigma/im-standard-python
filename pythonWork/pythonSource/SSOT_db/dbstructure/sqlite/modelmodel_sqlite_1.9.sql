-- Upgrade db to version 1.9

-- in case of violations during upgrade, switch constraints off and on again
PRAGMA ignore_check_constraints = ON;


--remove bure_role from table
create table businessrule_elements_tmp
    (
     bure_id integer not null primary key autoincrement,
     bure_buru_id numeric (10) not null ,
     bure_mode_id numeric (10) not null ,
     bure_writeable varchar (5) not null constraint ck__businessr__bure___10216507 check ( bure_writeable='TRUE' or bure_writeable='FALSE' ) ,
     bure_uc varchar (30) not null ,
     bure_dc varchar(30) not null ,
     bure_um varchar (30) null ,
     bure_dm varchar(30) ,
 	constraint bure_uk
 		unique (bure_buru_id,bure_mode_id),
	constraint bure_mode_fk foreign key(bure_mode_id)
		references modelelement (mode_id),
	constraint bure_buru_fk foreign key(bure_buru_id)
		references business_rules (buru_id) on delete cascade
);

insert into businessrule_elements_tmp (bure_id ,     bure_buru_id ,
     bure_mode_id ,     bure_writeable ,
     bure_uc ,     bure_dc ,
     bure_um ,     bure_dm)
	 select bure_id ,     bure_buru_id ,
     bure_mode_id ,     bure_writeable ,
     bure_uc ,     bure_dc ,
     bure_um ,bure_dm 
	 from businessrule_elements;

drop table businessrule_elements;
alter table businessrule_elements_tmp rename to businessrule_elements;

--remove checkconstraint from mode_type and melt_shortname
create table modelelement_tmp(
	mode_id integer not null
		primary key autoincrement,
	mode_type varchar(4) not null,
	mode_melt_id integer not null
		references modelelem_type (melt_id),
    mode_min_zoom_level numeric(1) null check ( mode_min_zoom_level between 0 and 4 ) ,
    mode_max_zoom_level numeric(1)  null check ( mode_max_zoom_level between 0 and 4 ) ,
	mode_publ_status varchar (5) null check ( mode_publ_status in ('DRAFT', 'GTOP', 'PUBL') )
);
insert into modelelement_tmp (mode_id ,mode_type,	mode_melt_id,mode_min_zoom_level,mode_max_zoom_level,mode_publ_status)
	select mode_id ,mode_type,	mode_melt_id,mode_min_zoom_level,mode_max_zoom_level,mode_publ_status from modelelement;
	
drop table modelelement;
alter table modelelement_tmp rename to modelelement;

create table modelelem_type_tmp
(
	melt_id integer not null
		primary key autoincrement,
	melt_shortname varchar(4) not null
		constraint melt_un unique,
	melt_name varchar(60) not null
		constraint melt_un2 unique,
	melt_uc varchar(30) not null,
	melt_dc varchar(30) not null,
	melt_um varchar(30),
	melt_dm varchar(30)
);
insert into modelelem_type_tmp (melt_id ,melt_shortname,melt_name,melt_uc,melt_dc,melt_um,melt_dm)
	select melt_id ,melt_shortname,melt_name,melt_uc,melt_dc,melt_um,melt_dm from modelelem_type;
	drop table modelelem_type;
	alter table modelelem_type_tmp rename to modelelem_type;

create table actor_roles 
    (
     actr_id integer not null primary key autoincrement
	 references modelelement (mode_id) 
	     on delete cascade,
     actr_name varchar (100) not null constraint actr_un unique, 
     actr_descr varchar (4000) , 
     actr_uc varchar (30) not null , 
     actr_dc datetime not null , 
     actr_um varchar (30) , 
     actr_dm datetime
	);

create table actor_concerns 
    (
     actc_id integer not null primary key autoincrement,
     actc_responsible varchar (5) not null default 'FALSE' check ( actc_responsible in ('FALSE', 'TRUE') ) , 
     actc_accountable varchar (5) not null default 'FALSE' check ( actc_accountable in ('FALSE', 'TRUE') ), 
     actc_consulted varchar (5) not null default 'FALSE' check ( actc_consulted in ('FALSE', 'TRUE') ) , 
     actc_informed varchar (5) not null default 'FALSE' check ( actc_informed in ('FALSE', 'TRUE') ) , 
     actc_actr_id numeric (10) not null , 
     actc_mode_id numeric (10) not null , 
     actc_uc varchar (30) not null , 
     actc_dc datetime not null , 
     actc_um varchar (30) , 
     actc_dm datetime,
	 constraint actc_uk unique (actc_actr_id, actc_mode_id),
	 constraint actc_actr_fk foreign key (actc_actr_id) 
	     references actor_roles (actr_id) 
	     on delete cascade,
	constraint actc_mode_id foreign key (actc_mode_id) 
		     references modelelement (mode_id) 
		     on delete cascade 
    );


drop view dbversion;
create view dbversion as select '1.9' as version, '2022-04-21 14:30' as installedtime;

PRAGMA ignore_check_constraints = OFF;

