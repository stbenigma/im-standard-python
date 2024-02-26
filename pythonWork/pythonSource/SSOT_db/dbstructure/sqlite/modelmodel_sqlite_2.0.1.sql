-- Upgrade db to version 2.0.1

-- in case of violations during upgrade, switch constraints off and on again
PRAGMA ignore_check_constraints = ON;

create table example_stories 
    (
     exst_id integer not null primary key autoincrement, 
     exst_no numeric (5) not null 
	 	constraint ck_exst_no check ( exst_no between 1 and 99999 ) , 
     exst_descr varchar (4000) , 
     exst_uc varchar (30) not null , 
     exst_dc varchar (30) not null , 
     exst_um varchar (30) , 
     exst_dm varchar (30),
	 constraint exst_un unique (exst_no)
    );

create table examples_temp 
	    (
	     expl_id integer not null primary key
			references modelelement (mode_id)
			on delete cascade,
	     expl_value varchar (4000) not null , 
	     expl_generated varchar (5) not null default 'FALSE' 
		 	constraint ck_expl_generated check ( expl_generated in ('TRUE','FALSE' )) , 
	     expl_enti_id numeric (10) , 
	     expl_attr_id numeric (10) , 
	     expl_rela_id numeric (10) , 
	     expl_rela_from varchar (5) 
			constraint ck_expl_relafrom check ((expl_rela_id is null and expl_rela_from is null) 
												or
												(expl_rela_id is not null 
													and expl_rela_from is not null
													and expl_rela_from in ('TRUE','FALSE')) 
												) , 
   	     expl_exst_id numeric (10) , 
	     expl_uc varchar (30) not null , 
	     expl_dc varchar(30) not null , 
	     expl_um varchar (30) , 
	     expl_dm varchar(30)
		 ,constraint fkarc_8 check ( 
		 	        (  (expl_enti_id is not null) and 
		 	         (expl_attr_id is null) and 
		 	         (expl_rela_id is null) ) or 
		 	        (  (expl_attr_id is not null) and 
		 	         (expl_enti_id is null) and 
		 	         (expl_rela_id is null) )  or 
		 	        (  (expl_rela_id is not null) and 
		 	         (expl_enti_id is null) and 
		 	         (expl_attr_id is null)  )  
				 )
		,constraint expl_enti_uk unique  (expl_value, expl_enti_id)
		,constraint expl_attr_uk unique  (expl_value, expl_attr_id)
		,constraint expl_rela_uk unique  (expl_value, expl_rela_id)
		,constraint expl_attr_fk foreign key (expl_attr_id) 
			references attributes (attr_id ) on delete cascade
		,constraint expl_enti_fk foreign key ( expl_enti_id) 
			references entities (enti_id ) on delete cascade
		,constraint expl_rela_fk foreign key ( expl_rela_id) 
				references relations (rela_id ) on delete cascade
		,constraint expl_exst_fk foreign key ( expl_exst_id) 
				references example_stories (exst_id ) on delete cascade
	    );

	insert into examples_temp  (expl_id,
     expl_value , 
     expl_generated , 
     expl_enti_id, 
     expl_attr_id, 
     expl_rela_id, 
     expl_rela_from, 
     expl_exst_id, 
     expl_uc, 
     expl_dc, 
     expl_um, 
     expl_dm)
		select expl_id,
	      expl_value , 
	      'FALSE' generated , 
	      expl_enti_id, 
	      expl_attr_id, 
	      null expl_rela_id, 
	      null expl_rela_from, 
	      null expl_exst_id, 
	      expl_uc, 
	      expl_dc, 
	      expl_um, 
	      expl_dm from examples;
	

	drop table examples;
	alter table examples_temp rename to examples;


drop view dbversion;
create view dbversion as select '2.0.1' as version, '2022-10-06 10:00' as installedtime;

PRAGMA ignore_check_constraints = OFF;

