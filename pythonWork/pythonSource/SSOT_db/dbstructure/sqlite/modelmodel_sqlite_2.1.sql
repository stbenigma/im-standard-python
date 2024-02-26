-- Upgrade db to version 2.1

-- in case of violations during upgrade, switch constraints off and on again
PRAGMA ignore_check_constraints = ON;


create table linesegments_temp
(
	lise_id integer
		primary key autoincrement,
	lise_seq integer not null,
	lise_relr_id integer not null
		references relationreps (relr_id)
			on delete cascade,
	lise_x integer not null,
	lise_y integer not null,
	lise_linetype VARCHAR2(6) default 'SOLID',
	lise_angle integer,
	constraint lise__un
		unique (lise_relr_id, lise_seq),
	constraint ck_lise_linetype
		check (lise_linetype IN('DADO','DASHED','DOTTED','SOLID')),
	constraint lise_angle_chk
			check (lise_angle BETWEEN -3.1415926535898 AND 3.141592653589793),
    CONSTRAINT ck_lise_x CHECK(lise_x BETWEEN 0 AND 999999) ,
	constraint ck_lise_y check (lise_y BETWEEN 0 AND 999999)
);


insert into linesegments_temp
    select lise_id ,lise_seq ,lise_relr_id,
	lise_x ,lise_y,lise_linetype ,lise_angle
    from linesegments;
drop table linesegments;
alter table linesegments_temp rename to linesegments;

create table columns_temp
(
	colu_id integer
		primary key
		constraint colu_mode_fk
			references MODELELEMENT (mode_id)
		on delete cascade,
	colu_column_name varchar(60) not null,
	colu_mandatory varchar(5) not null,
	colu_format varchar(200),
	colu_ext_system_id varchar(100),
	colu_descr varchar(4000),
	colu_type_string varchar(200),
    colu_read VARCHAR (5) NOT NULL DEFAULT 'TRUE' CHECK ( colu_read IN ('FALSE', 'TRUE') ) ,
    colu_update VARCHAR (5) NOT NULL DEFAULT 'FALSE' CHECK ( colu_update IN ('FALSE', 'TRUE') ),
	colu_tabl_id integer not null
		constraint colu_tabl_fk
			references tables (tabl_id),
	colu_doma_id integer
		constraint colu_doma_fk
			references DOMAINS (doma_id),
	colu_uc varchar(30) not null,
	colu_dc varchar(30) not null,
	colu_um varchar(30),
	colu_dm varchar(30),
	constraint colu_uk
		unique (colu_tabl_id, colu_column_name),
	check (colu_mandatory in ('TRUE', 'FALSE'))
);

insert into columns_temp
    select * from columns;
drop table columns;
alter table columns_temp rename to columns;

create table attributes_temp
(
	attr_id integer not null
		primary key
		references modelelement (mode_id)			on delete cascade,
	attr_enti_id integer not null		references entities (enti_id),
	attr_doma_id integer 	references domains (doma_id),
	attr_tech_name varchar(60) not null,
	attr_displ_name varchar(4000),
	attr_displ_seq numeric(5),
	attr_tooltip varchar(4000),
	attr_descr varchar(4000),
	attr_is_descriptive varchar(5) not null,
	attr_is_mandatory varchar(5) not null,
	attr_is_historicised varchar(5) not null,
	attr_is_repeated varchar(5) not null,
	attr_is_translated varchar(5) not null,
	attr_is_encrypted varchar(5) not null,
	attr_uc varchar(30) not null,
	attr_dc varchar(30) not null,
	attr_um varchar(30),
	attr_dm varchar(30),
	constraint attr_uk	unique (attr_tech_name, attr_enti_id),
	constraint attr_uk2	unique (attr_displ_name, attr_enti_id),
	check (attr_is_descriptive in('FALSE','TRUE')),
	check (attr_is_encrypted in('FALSE','TRUE')),
	check (attr_is_historicised in('FALSE','TRUE')),
	check (attr_is_mandatory in('FALSE','TRUE')),
	check (attr_is_repeated in('FALSE','TRUE')),
	check (attr_is_translated in('FALSE','TRUE'))
);

insert into attributes_temp
    select * from attributes;
drop table attributes;
alter table attributes_temp rename to attributes;

create table datamodels
(
	datm_id integer
		primary key autoincrement
		references modelelement (mode_id)
		on delete cascade,
	datm_name varchar(60) not null
		constraint datm_un unique,
	datm_descr varchar(4000),
	datm_uc varchar(30) not null,
	datm_dc varchar(30) not null,
	datm_um varchar(30),
	datm_dm varchar(30)
);
insert into datamodels 
    select * from interfaces;
    
drop table interfaces;

create table tables_temp
(
	tabl_id integer
		primary key autoincrement
		constraint TABL_MODE_FK
			references MODELELEMENT (mode_id)
		on delete cascade,
	tabl_name varchar(60) not null,
	tabl_datm_id integer not null
		references datamodels (datm_ID),
	tabl_prefix varchar(60),
	tabl_descr varchar(4000),
tabl_create varchar (5) not null default 'FALSE' check ( tabl_create in ('FALSE', 'TRUE') ) , 
tabl_read varchar (5) not null default 'TRUE' check ( tabl_read in ('FALSE', 'TRUE') ) , 
tabl_update varchar (5) not null default 'FALSE' check ( tabl_update in ('FALSE', 'TRUE') ) , 
tabl_delete varchar (5) not null default 'FALSE' check ( tabl_delete in ('FALSE', 'TRUE') ) ,
	tabl_uc varchar(30) not null,
	tabl_dc varchar(30) not null,
	tabl_um varchar(30),
	tabl_dm varchar(30),
	constraint TABL_UN
		unique (tabl_datm_id, tabl_name)
);
insert into tables_temp
    select * from tables;
drop table tables;
alter table tables_temp rename to tables;


create table domains_temp
(
	doma_id integer not null
		primary key
		references modelelement (mode_id)
		on delete cascade,
	doma_name varchar(60) not null
		constraint doma_name_uk unique,
	doma_descr varchar(4000),
	doma_type varchar(4) not null,
	doma_origin varchar(6) not null,
	doma_datm_id integer
		constraint doma_datm_fk
			references datamodels (datm_id),
	doma_daty_id integer
		references datatypes (daty_id) ,
	doma_dat_minvalue varchar(30),
	doma_dat_maxvalue varchar(30),
	doma_dat_granularity varchar(15),
	doma_txt_maxlng numeric(28),
	doma_txt_syntaxrule varchar(4000),
	doma_num_maxvalue numeric(30,10),
	doma_num_minvalue numeric(30,10),
	doma_num_total_digits numeric(3),
	doma_num_fract_digits numeric(3) ,
	doma_num_round_value numeric(7,3),
	doma_num_phyu_id integer
		references physical_unit (phyu_id),
	doma_bin_contenttype varchar(30),
	doma_bin_stfo_id integer
		references storage_formats (stfo_id),
	doma_uc varchar(30) not null,
	doma_dc varchar(30) not null,
	doma_um varchar(30),
	doma_dm varchar(30),
	check (doma_bin_contenttype in ('DRAWING', 'FILM', 'IMAGE', 'OTHER', 'SOUND', 'TEXT')),
	check (doma_dat_granularity IN ('DAY', 'HOUR', 'MILlISECOND', 'MINUTE', 'MONTH', 'QUARTER', 'SECOND', 'SEMESTER', 'WEEK', 'YEAR')),
	check (doma_origin IN ('DER', 'DOM')),
	check (doma_type IN ('BIN', 'DAT', 'GRP', 'LOV', 'NUM', 'TXT')),
	constraint doma_exdep1
		check (doma_type != 'BIN'
 or ( doma_bin_contenttype is not null and doma_num_fract_digits is null and doma_num_maxvalue is null and doma_num_minvalue is null
	 and doma_num_phyu_id is null and doma_num_round_value is null and doma_num_total_digits is null and doma_dat_granularity is null
	 and doma_dat_maxvalue is null and doma_dat_minvalue is null and doma_txt_syntaxrule is null and doma_txt_maxlng is null)),
	constraint doma_exdep2
		check (doma_type != 'DAT'
 or ( doma_bin_contenttype is null and doma_bin_stfo_id is null and doma_num_fract_digits is null
	 and doma_num_maxvalue is null and doma_num_minvalue is null and doma_num_phyu_id is null and doma_num_round_value is null
	 and doma_num_total_digits is null and doma_dat_granularity is not null and doma_txt_syntaxrule is null and doma_txt_maxlng is null)),
	constraint doma_exdep3
		check (doma_type != 'GRP'
 or ( doma_bin_contenttype is null and doma_bin_stfo_id is null and doma_num_fract_digits is null and doma_num_maxvalue is null and doma_num_minvalue is null and doma_num_phyu_id is null and doma_num_round_value is null and doma_num_total_digits is null and doma_dat_granularity is null and doma_dat_maxvalue is null and doma_dat_minvalue is null and doma_txt_syntaxrule is null and doma_txt_maxlng is null)),
	constraint doma_exdep4
		check (doma_type != 'LOV'
 or ( doma_bin_contenttype is null and doma_bin_stfo_id is null and doma_num_fract_digits is null and doma_num_maxvalue is null and doma_num_minvalue is null and doma_num_phyu_id is null and doma_num_round_value is null and doma_num_total_digits is null and doma_dat_granularity is null and doma_dat_maxvalue is null and doma_dat_minvalue is null and doma_txt_syntaxrule is null)),
	constraint doma_exdep5
		check (doma_type != 'NUM'
 or ( doma_bin_contenttype is null and doma_bin_stfo_id is null and doma_dat_granularity is null and doma_dat_maxvalue is null and doma_dat_minvalue is null and doma_txt_syntaxrule is null and doma_txt_maxlng is null)),
	constraint doma_exdep6
		check (doma_type != 'TXT'
 or ( doma_bin_contenttype is null and doma_bin_stfo_id is null and doma_num_fract_digits is null and doma_num_maxvalue is null and doma_num_minvalue is null and doma_num_phyu_id is null and doma_num_round_value is null and doma_num_total_digits is null and doma_dat_granularity is null and doma_dat_maxvalue is null and doma_dat_minvalue is null))
,constraint doma_num_1 check ( doma_num_minvalue is null
			or doma_num_maxvalue is null or doma_num_minvalue <= doma_num_maxvalue )
,constraint doma_num_2 check ( doma_num_fract_digits is null or doma_num_total_digits is null or doma_num_fract_digits <= doma_num_total_digits)
);

insert into domains_temp
    select * from domains;
drop table domains;
alter table domains_temp rename to domains;

create table systems
(
	syst_id integer not null
		primary key
		references modelelement (mode_id)
		on delete cascade,
	syst_name varchar(60) not null
		constraint syst_name_uk
			unique,
	syst_short_name varchar(60),
	syst_descr varchar(4000),
	syst_uc varchar(30) not null,
	syst_dc varchar(30) not null,
	syst_um varchar(30),
	syst_dm varchar(30)
);

create table mappings
(
	maps_id integer not null
		primary key
		references modelelement (mode_id)
		on delete cascade,
	maps_name varchar(60) not null,
	maps_type varchar(10) not null
	    constraint  type_chk check (maps_type in ('DATM-IM',
	                                    'DATM-DATM',
	                                    'DOMA-DOMA',
	                                   'DATM-SYST'
	                                    )
	                        ),
    maps_mode_id1 integer not null
		constraint maps_mode_fk1
			references modelelement (mode_id)
				on delete cascade,
    maps_mode_id2 integer
		constraint maps_mode_fk2
			references modelelement (mode_id)
				on delete cascade,
	maps_descr varchar(4000),
    maps_rule_frwd  varchar(4000),
    maps_rule_bckw  varchar(4000),
	maps_uc varchar(30) not null,
	maps_dc varchar(30) not null,
	maps_um varchar(30),
	maps_dm varchar(30)
);

create table mode_mode_maps
(
	momo_id INTEGER
		primary key autoincrement,
    momo_maps_id integer not null
	constraint momo_maps_fk
		references mappings (maps_id)
			on delete cascade,
	momo_mode_id1 INTEGER not null
	constraint momo_mode_fk1
		references modelelement (mode_id)
			on delete cascade,
	momo_mode_id2 INTEGER not null
		constraint momo_mode_fk2
			references modelelement (mode_id)
				on delete cascade,
    momo_sub_enti_id INTEGER
    	constraint momo_enti_fk
    	references entities (enti_id),
    momo_descr varchar(4000),
    momo_onedirection varchar(5) default 'TRUE' not null
	    check (momo_onedirection in('TRUE','FALSE')),
    momo_rule_frwd  varchar(4000),
    momo_rule_bckw  varchar(4000),
	momo_uc varchar(30) not null,
	momo_dc varchar(30) not null,
	momo_um varchar(30),
	momo_dm varchar(30),
    constraint momo_directchk check (momo_rule_bckw is null
                                         or momo_onedirection = 'FALSE'),
	constraint momo_uncomb
		unique (momo_mode_id1, momo_mode_id2)
);

create table deva_deva_maps
    (
    	dede_id INTEGER
    		primary key autoincrement,
        dede_maps_id integer not null
        constraint dede_maps_fk1
    		references mappings (maps_id)
    			on delete cascade,
    	dede_deva_id1 INTEGER not null
		constraint dede_deva_fk1
    		references default_values (deva_id)
    			on delete cascade,
    	dede_deva_id2 INTEGER not null
    		constraint dede_deva_fk2
    			references default_values (deva_id)
    				on delete cascade,
        dede_descr varchar(4000),
        dede_rule_frwd  varchar(4000),
        dede_rule_bckw  varchar(4000),
    	dede_uc varchar(30) not null,
    	dede_dc varchar(30) not null,
    	dede_um varchar(30),
    	dede_dm varchar(30),
    	constraint dede_uncomb
    		unique (dede_deva_id1, dede_deva_id2)
    );
    
    
delete  from mappings;
insert into mappings (maps_name, maps_type,
                      maps_mode_id1,
                      maps_uc,maps_dc)
select distinct datm_name || '-' || 'IM' maps_name,
                'DATM-IM' maps_type,
       tabl_datm_id maps_mode_id1,
       'SYS', datetime()
from tabl_enti_maps
join tables on tabl_id = tema_tabl_id
join datamodels on datm_id = tabl_datm_id
;

delete  from mode_mode_maps;
insert into mode_mode_maps (momo_maps_id,
                            momo_mode_id1,
                            momo_mode_id2,
                            momo_onedirection,
                            momo_uc,
                            momo_dc)
select  maps_id maps_id,
       tema_tabl_id momo_mode_id1,
       coalesce(tema_enti_id,tema_rela_id) momo_mode_id2,
       'TRUE' momo_onedirection,
       'SYS' momo_uc,
       datetime() momo_dc
from tabl_enti_maps
    join tables on tabl_id = tema_tabl_id
    join  mappings on maps_mode_id1 = tabl_datm_id
;

insert into mode_mode_maps (momo_maps_id,
                            momo_mode_id1,
                            momo_mode_id2,
                            momo_sub_enti_id,
                            momo_onedirection,
                            momo_uc,
                            momo_dc)
select maps_id momo_maps_id,
       coam_colu_id momo_mode_id1,
       coam_attr_id momo_mode_id2,
       coam_enti_id momo_subenti_id,
       'TRUE' momo_onedirection,
       'SYS' momo_uc,
       datetime() momo_dc
from colu_attr_map
    join columns on colu_id = coam_colu_id
    join tables on tabl_id = colu_tabl_id
    join mappings on  maps_mode_id1 = tabl_datm_id
        and mappings.maps_type = 'DATM-IM'
;

drop table colu_attr_map;
drop view if exists colu_attr_map ;
create view colu_attr_map as
    select momo_id coam_id,
       0 coam_seq,
       "INBOUND" coam_direction,
       momo_rule_frwd coam_transf_rule,
       null coam_triggertype,
       null coam_triggerperiod,
       colu_id coam_colu_id,
       attr_id coam_attr_id,
       momo_sub_enti_id coam_enti_id,
       momo_rule_bckw coam_transf_rule_bckw,
       momo_onedirection coam_onedirection,
       momo_descr coam_descr,
       momo_maps_id coam_maps_id,
       momo_uc coam_uc,
       momo_dc coam_dc,
       momo_um coam_um,
       momo_dm coam_dm
from mode_mode_maps
join columns on colu_id = momo_mode_id1
join attributes on attr_id = momo_mode_id2;


drop table tabl_enti_maps;
drop view if exists tabl_enti_maps;
create view tabl_enti_maps as
    select momo_id tema_id,
       momo_mode_id1 tema_tabl_id,
       momo_mode_id2 tema_enti_id,
       null tema_rela_id,
       momo_rule_frwd tema_transf_rule_frwd,
       momo_rule_bckw tema_transf_rule_bckw,
       momo_onedirection tema_onedirection,
       momo_descr tema_descr,
       momo_maps_id tema_maps_id,
       momo_uc tema_uc,
       momo_dc tema_dc,
       momo_um tema_um,
       momo_dm tema_dm
from mode_mode_maps
join tables on tabl_id = momo_mode_id1
join entities on enti_id = momo_mode_id2
union all
select momo_id tema_id,
       momo_mode_id1 tema_tabl_id,
       null tema_enti_id,
       momo_mode_id2 tema_rela_id,
       momo_rule_frwd tema_transf_rule_frwd,
       momo_rule_bckw tema_transf_rule_bckw,
       momo_onedirection tema_onedirection,
       momo_descr tema_descr,
       momo_maps_id tema_maps_id,
       momo_uc tema_uc,
       momo_dc tema_dc,
       momo_um tema_um,
       momo_dm tema_dm
from mode_mode_maps
join tables on tabl_id = momo_mode_id1
join relations on rela_id = momo_mode_id2;

UPDATE modelelem_type SET melt_name = 'Datatype', melt_um = 'SYS', melt_dc = '2023-12-29' WHERE melt_shortname = 'DATY';


drop view if exists dbversion;
create view dbversion as select '2.1' as version, '2023-09-02 10:00' as installedtime;

PRAGMA ignore_check_constraints = OFF;

