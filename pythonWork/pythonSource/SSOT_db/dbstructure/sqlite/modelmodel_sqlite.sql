create table languages
(
	lang_id integer not null
		primary key autoincrement,
	lang_iso_name varchar(60)
		constraint lang_iso_name_un unique,
	lang_iso_code2 char(2) not null
		constraint lang_iso_code2_un unique,
	lang_iso_code3 char(3) not null
		constraint lang_iso_code3_un unique,
	lang_is_text_lang varchar(5) not null,
	lang_is_base_lang varchar(5) not null,
	lang_lang_id integer
		references languages (lang_id)
			on delete set null,
	lang_uc varchar(30) not null,
	lang_dc varchar(30) not null,
	lang_um varchar(30),
	lang_dm varchar(30),
	check (lang_is_base_lang in ('FALSE', 'TRUE')),
	check (lang_is_text_lang in ('FALSE', 'TRUE')),
	constraint lang_iso2_chk
		check (lang_iso_code2 = lower(lang_iso_code2)),
	constraint lang_iso3_chk
		check (lang_iso_code3 = lower(lang_iso_code3))
);

create table modelelem_type
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

create table modelelement
(
	mode_id integer not null
		primary key autoincrement,
	mode_type varchar(4) not null,
	mode_melt_id integer not null
		references modelelem_type (melt_id),
    mode_min_zoom_level numeric(1) null check ( mode_min_zoom_level between 0 and 4 ) ,
    mode_max_zoom_level numeric(1)  null check ( mode_max_zoom_level between 0 and 4 ) ,
	mode_publ_status varchar (5) null check ( mode_publ_status in ('DRAFT', 'GTOP', 'PUBL') )
);

create table datatypes
(
	daty_id integer not null
		primary key
		references modelelement (mode_id)
		on delete cascade,
	daty_name varchar(60) not null
		constraint dati_un unique,
	daty_basetype varchar(60) not null,
	daty_uc varchar(30) not null,
	daty_dc varchar(30) not null,
	daty_um varchar(30),
	daty_dm varchar(30),
	constraint daty_basetype_ck
		check (daty_basetype in ('BINARY', 'NUMERIC', 'STRING', 'DATETIME'))
);

create table entity_categories
    (
     enca_id integer not null
        primary key,
     enca_name varchar (60) not null
        constraint enca_uk unique ,
     enca_uc varchar (30) not null ,
     enca_dc varchar (30) not null ,
     enca_um varchar (30) null ,
     enca_dm varchar (30) null
);

create table entities
(
	enti_id integer not null
		primary key
		references modelelement (mode_id)
		on delete cascade,
	enti_name varchar(60) not null
		constraint enti_name_uk
			unique,
    enti_enca_id numeric (10) null
        references entity_categories (enca_id),
    enti_underlay_enti_id numeric (10) null
        references entities (enti_id),
	enti_short_name varchar(60),
	enti_prefix varchar(60),
	enti_tooltip varchar(4000),
	enti_descr varchar(4000),
	enti_exp_tuplecnt varchar(100),
	enti_uc varchar(30) not null,
	enti_dc varchar(30) not null,
	enti_um varchar(30),
	enti_dm varchar(30)
);

create table arcs
(
	arcs_id integer not null
		primary key autoincrement
		references modelelement (mode_id)
			on delete cascade,
	arcs_name varchar(60) not null,
	arcs_enti_id integer not null
		references entities (enti_id)
			on delete cascade,
	arcs_uc varchar(30) not null,
	arcs_dc varchar(30) not null,
	arcs_um varchar(30),
	arcs_dm varchar(30),
	constraint arcs_uk
		unique (arcs_enti_id, arcs_name)
);

create table external_refs
(
	extr_id integer not null
		primary key autoincrement,
	extr_source_name varchar(60) not null,
	extr_source_id varchar(100) not null,
	extr_mode_id integer not null
		references modelelement (mode_id)
			on delete cascade,
	extr_last_update varchar(30) not null,
	constraint extr_uk
		unique (extr_source_name, extr_mode_id),
	constraint extr_uk_id
		unique (extr_source_name, extr_source_id)
);

create table keys
(
	keys_id integer not null
		primary key autoincrement
		references modelelement (mode_id)
			on delete cascade,
	keys_name varchar(60) not null,
	keys_enti_id integer not null
		references entities (enti_id)
			on delete cascade,
	keys_uc varchar(30) not null,
	keys_dc varchar(30) not null,
	keys_um varchar(30),
	keys_dm varchar(30),
	constraint keys_uk
		unique (keys_enti_id, keys_name)
);

create table lang_texts
(
	lgtx_id integer not null
		primary key autoincrement,
	lgtx_attrname varchar(60) not null,
	lgtx_text varchar(4000),
	lgtx_lang_id integer not null
		references languages (lang_id),
	lgtx_mode_id integer not null
		references modelelement (mode_id)
			on delete cascade,
	lgtx_uc varchar(30) not null,
	lgtx_dc varchar(30) not null,
	lgtx_um varchar(30),
	lgtx_dm varchar(30),
	constraint lgtx_uk
		unique (lgtx_lang_id, lgtx_mode_id, lgtx_attrname)
);

create table physical_unit
(
	phyu_id integer not null
		primary key autoincrement,
	phyu_si_unit varchar(10)
		constraint phyu_uk_siunit unique,
	phyu_name varchar(60) not null
		constraint phyu_uk_name unique,
	phyu_descr varchar(4000),
	phyu_uc varchar(30) not null,
	phyu_dc varchar(30) not null,
	phyu_um varchar(30),
	phyu_dm varchar(30)
);

create table relations
(
	rela_id integer not null
		primary key
		references modelelement (mode_id)
		on delete cascade,
	rela_name varchar(60) not null
		constraint rela_uk_name unique,
	rela_type varchar(4) not null,
	rela_enti_id_from integer not null
		references entities (enti_id),
	rela_arcs_id_from integer
		references arcs (arcs_id)
			on delete set null,
	rela_assoc_from_to varchar(4000),
	rela_maptype_from_to char(1) not null,
	rela_mandatory_from_to varchar(5) not null,
	rela_hist_from_to varchar(5) not null,
	rela_enti_id_to integer not null
		references entities (enti_id),
	rela_arcs_id_to integer
		references arcs (arcs_id)
			on delete set null,
	rela_assoc_to_from varchar(100),
	rela_maptype_to_from char(1) not null,
	rela_mandatory_to_from varchar(5) not null,
	rela_hist_to_from varchar(4000) not null,
	rela_uc varchar(30) not null,
	rela_dc varchar(30) not null,
	rela_um varchar(30),
	rela_dm varchar(30),
	check (rela_hist_from_to in('FALSE','TRUE')),
	check (rela_hist_to_from in('FALSE','TRUE')),
	check (rela_mandatory_from_to in('FALSE','TRUE')),
	check (rela_mandatory_to_from in('FALSE','TRUE')),
	check (rela_maptype_from_to in ('1', 'M')),
	check (rela_maptype_to_from in ('1', 'M')),
	check (RELA_TYPE IN ('1:1', 'ISAR', 'ISAS', 'M:1', 'M:N')),
	constraint rela_maptype_chk
		check ((rela_type = 'ISAR'
  and rela_maptype_from_to = '1'
  and rela_maptype_to_from = '1'
  and (rela_mandatory_from_to = 'TRUE'
  	  or
  	  rela_mandatory_to_from = 'TRUE'
  	  )
) or
(rela_type = 'ISAS'
  and rela_maptype_from_to = '1'
  and rela_maptype_to_from = '1'
  and rela_mandatory_from_to = 'TRUE'
  and rela_mandatory_to_from = 'TRUE'
  and (rela_arcs_id_from is not null
  		or
	   rela_arcs_id_to is not null
	  )
) or
(rela_type = '1:1'
  and rela_maptype_from_to = '1'
  and rela_maptype_to_from = '1'
) or
(rela_type ='M:1'
  and (
  	(rela_maptype_from_to = '1'
 	 and rela_maptype_to_from = 'M'
  	) OR
  	(rela_maptype_from_to = 'M'
  	 and rela_maptype_to_from = '1'
	)
  )
) or
(rela_type = 'M:N'
  and rela_maptype_to_from = 'M'
  and rela_maptype_from_to = 'M'
))
);

create table storage_formats
(
	stfo_id integer not null
		primary key autoincrement,
	stfo_name varchar(60) not null
		constraint stfo_un unique,
	stfo_descr varchar(4000),
	stfo_uc varchar(30) not null,
	stfo_dc varchar(30) not null,
	stfo_um varchar(30),
	stfo_dm varchar(30)
);

create table documents
(
	docu_id integer not null
		primary key
		references modelelement (mode_id)
		on delete cascade,
	docu_name varchar(60) not null constraint docu_uk unique,
	docu_stfo_id integer
		references storage_formats (stfo_id),
	docu_reference varchar(500),
	docu_content blob,
	docu_docu_id integer
		references documents (docu_id)
);

create table mode_docu
(
	modo_id integer not null
		primary key autoincrement,
	modo_mode_id integer not null
		references modelelement (mode_id)
			on delete cascade,
	modo_docu_id integer not null
		references documents (docu_id)
			on delete cascade,
	constraint modo_uk
		unique (modo_mode_id, modo_docu_id)
);

create table synonyms
(
	syno_id integer not null
		primary key
		references modelelement (mode_id)
		on delete cascade,
	syno_name varchar(60) not null,
	syno_enti_id integer not null
		references entities (enti_id)
			on delete cascade,
	syno_uc varchar(30) not null,
	syno_dc varchar(30) not null,
	syno_um varchar(30),
	syno_dm varchar(30),
	constraint syno_uk unique (syno_enti_id,syno_name)
);

create table user_defined_properties
(
	udpr_id integer not null
		primary key autoincrement,
	udpr_theme varchar(60) not null,
	udpr_group varchar(60),
	udpr_name varchar(60) not null,
	udpr_descr varchar(4000),
    udpr_defaultvalue varchar (4000) ,
	udpr_uc varchar(30) not null,
	udpr_dc varchar(30) not null,
	udpr_um varchar(30),
	udpr_dm varchar(30),
	constraint udpr_un
		unique (udpr_theme, udpr_name)
);

create table modelemtype_properties
(
	metp_id integer not null
		primary key autoincrement,
	metp_melt_id integer not null
		references modelelem_type (melt_id)
            on delete cascade,
	metp_udpr_id integer not null
		references user_defined_properties (udpr_id)
            on delete cascade,
	metp_optional varchar(5) not null,
	constraint metp_un
		unique (metp_melt_id, metp_udpr_id),
	check (metp_optional in ('FALSE', 'TRUE'))
);

create table udp_values
(
	udpv_id integer not null
		primary key autoincrement,
	udpv_value varchar(4000),
	udpv_mode_id integer not null
		references modelelement (mode_id)
			on delete cascade,
	udpv_udpr_id integer not null
		references user_defined_properties (udpr_id)
            on delete cascade,
	udpv_uc varchar(30) not null,
	udpv_dc varchar(30) not null,
	udpv_um varchar(30),
	udpv_dm varchar(30),
	constraint udpv_un
		unique (udpv_mode_id, udpv_udpr_id)
);

create table diagramtypes
(
	diat_id integer
		primary key autoincrement,
	diat_name varchar(100) not null
		constraint diat_un unique,
	diat_uc varchar(30) not null,
	diat_dc varchar(30) not null,
	diat_um varchar(30),
	diat_dm varchar(30)
);

create table diagrams
(
	diag_id integer
		primary key autoincrement
		references MODELELEMENT (mode_id)
		on delete cascade,
	diag_name varchar(60) not null
		constraint diag__un unique,
	diag_diat_id integer not null
		references diagramtypes (diat_id),
	diag_legendx integer,
	diag_legendy integer,
	diag_uc varchar(30) not null,
	diag_dc varchar(30) not null,
	diag_um varchar(30),
	diag_dm varchar(30)
);

create table elementreps
(
	eler_id integer
		primary key autoincrement,
	eler_mode_id integer not null
		constraint eler_mode_fk
			references MODELELEMENT (mode_id)
				on delete cascade,
	eler_diag_id integer not null
		references diagrams (diag_id)
			on delete cascade,
	eler_index NUMBER(4) default 0 not null,
	eler_position_x integer,
	eler_position_y integer,
	eler_width integer not null,
	eler_height integer not null,
	eler_opacity integer,
	eler_color varchar(6) not null,
	eler_marginwidth integer,
	eler_marginopacity integer,
	eler_margincolor varchar(6),
	eler_fontsize integer,
	eler_fontcolor varchar(6),
	eler_uc varchar(30) not null,
	eler_dc varchar(30) not null,
	eler_um varchar(30),
	eler_dm varchar(30),
	constraint eler_un
		unique (eler_diag_id, eler_mode_id, eler_index),
	check (eler_fontsize between 1 and 999),
	check (eler_marginopacity between 0 and 100),
	check (eler_opacity between 0 and 100),
	check (length(eler_color)= 6),
	check (length(eler_fontcolor)= 6),
	check (length(eler_margincolor)= 6)
);

create table interfaces
(
	intf_id integer
		primary key autoincrement
		references modelelement (mode_id)
		on delete cascade,
	intf_name varchar(60) not null
		constraint intf_un unique,
	intf_descr varchar(4000),
	intf_uc varchar(30) not null,
	intf_dc varchar(30) not null,
	intf_um varchar(30),
	intf_dm varchar(30)
);

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



create table domains
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
	doma_intf_id integer
		constraint doma_intf_fk
			references interfaces (intf_id),
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
 or ( doma_bin_contenttype is null and doma_bin_stfo_id is null and doma_num_fract_digits is not null and doma_num_total_digits is not null and doma_dat_granularity is null and doma_dat_maxvalue is null and doma_dat_minvalue is null and doma_txt_syntaxrule is null and doma_txt_maxlng is null)),
	constraint doma_exdep6
		check (doma_type != 'TXT'
 or ( doma_bin_contenttype is null and doma_bin_stfo_id is null and doma_num_fract_digits is null and doma_num_maxvalue is null and doma_num_minvalue is null and doma_num_phyu_id is null and doma_num_round_value is null and doma_num_total_digits is null and doma_dat_granularity is null and doma_dat_maxvalue is null and doma_dat_minvalue is null))
);

create table attributes
(
	attr_id integer not null
		primary key
		references modelelement (mode_id)			on delete cascade,
	attr_enti_id integer not null		references entities (enti_id),
	attr_doma_id integer not null		references domains (doma_id),
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

create table default_values
(
	deva_id integer not null
		primary key autoincrement,
	deva_doma_id integer not null
		references domains (doma_id)
			on delete cascade,
	deva_value varchar(100) not null,
	deva_sort_order numeric(3),
	deva_displ varchar(4000),
	deva_descr varchar(4000),
	deva_uc varchar(30) not null,
	deva_dc varchar(30) not null,
	deva_um varchar(30),
	deva_dm varchar(30),
	constraint deva_uk
		unique (deva_doma_id, deva_value)
);

create table domaingroup_members
(
	dgrm_id integer not null
		primary key autoincrement
		references modelelement (mode_id)
		on delete cascade,
	dgrm_name varchar(4000) not null,
	dgrm_descr varchar(4000),
	dgrm_is_mandatory varchar(5) not null,
	dgrm_doma_id_group integer not null
		references domains (doma_id) on delete cascade,
	dgrm_doma_id_member integer not null
		references domains (doma_id),
	dgrm_uc varchar(30) not null,
	dgrm_dc varchar(30) not null,
	dgrm_um varchar(30),
	dgrm_dm varchar(30),
	constraint dgrm_doma_uk
		unique (dgrm_doma_id_group, dgrm_name),
	check (dgrm_is_mandatory in ('FALSE', 'TRUE'))
);

create table key_elements
(
	kele_id integer not null
		primary key autoincrement,
	kele_keys_id integer not null
		references keys (keys_id)
			on delete cascade,
	kele_attr_id integer
		references attributes (attr_id)
			on delete cascade,
	kele_rela_id integer
		references relations (rela_id)
			on delete cascade,
	kele_uc varchar(30) not null,
	kele_dc varchar(30) not null,
	kele_um varchar(30),
	kele_dm varchar(30),
	constraint kele_attr_un
		unique (kele_keys_id, kele_attr_id),
	constraint kele_rela_un
			unique (kele_keys_id, kele_rela_id),
	constraint fkarc_8
		check (( (kele_rela_id is not null) and
		   (kele_attr_id is null)
	     ) or (  (kele_attr_id is not null) and
                 (kele_rela_id is null) ))
);

create table melt_diats
(
	medi_id integer
		primary key autoincrement,
	medi_diat_id integer not null
		references diagramtypes (diat_id)
			on delete cascade,
	medi_melt_id integer not null
		constraint modi_melt_fk
			references MODELELEM_TYPE (melt_id)
				on delete cascade,
	medi_uc varchar(30) not null,
	medi_dc varchar(30) not null,
	medi_um varchar(30),
	medi_dm varchar(30),
	constraint medi__un
		unique (medi_diat_id, medi_melt_id)
);

create table organisationalunits
(
	orgu_id integer
		primary key
		constraint orgu_mode_fk
			references MODELELEMENT (mode_id)
		on delete cascade,
	orgu_name VARCHAR(60) not null
		constraint orgu_name_un unique,
	orgu_descr VARCHAR(4000),
	orgu_mail VARCHAR(200),
	orgu_telefon VARCHAR(30),
	orgu_address VARCHAR(4000),
	orgu_orgu_id NUMBER(10)
		references organisationalunits (orgu_id)
			on delete set null,
	orgu_uc varchar(30) not null,
	orgu_dc varchar(30) not null,
	orgu_um varchar(30),
	orgu_dm varchar(30)
);

create table mode_orgu
(
	moou_id integer
		primary key,
	moou_mode_id integer not null
		constraint moou_mode_fk
			references MODELELEMENT (mode_id)
				on delete cascade,
	moou_orgu_id integer not null
		references organisationalunits (orgu_id)
			on delete cascade
);

create table projects
(
	proj_id integer
		primary key autoincrement,
	proj_name VARCHAR(60) not null
		constraint proj__un unique,
	proj_languages VARCHAR(60),
	proj_curr_lang VARCHAR2(2),
	proj_uc VARCHAR(30) not null,
	proj_dc VARCHAR(30) not null,
	proj_um VARCHAR(30),
	proj_dm VARCHAR(30)
);

create table relationreps
(
	relr_id integer
		primary key autoincrement,
	relr_diag_id integer not null
		references diagrams (diag_id)
				on delete cascade,
	relr_mode_id integer not null
		constraint relr_mode_fk
			references MODELELEMENT (mode_id)
				on delete cascade,
	relr_linewidth integer default 1 not null,
	relr_linecolor varchar(6) default '000000' ,
	relr_lineopacity integer default 100,
	relr_startedge varchar(1),
	relr_startposition integer,
	relr_start_connector VARCHAR2(1),
	relr_starttext_angle integer,
	relr_starttext_distance integer,
	relr_starttext_x integer,
	relr_starttext_y integer,
	relr_starttext_width integer,
	relr_starttext_height integer,
	relr_endedge varchar(1),
	relr_endposition integer,
	relr_end_connector VARCHAR2(1),
	relr_endtext_angle integer,
	relr_endtext_distance integer,
	relr_endtext_x integer,
	relr_endtext_y integer,
	relr_endtext_width integer,
	relr_endtext_height integer,
	relr_fontcolor varchar(6) default '000000',
	relr_fontsize integer,
	relr_uc varchar(30) not null,
	relr_dc varchar(30) not null,
	relr_um varchar(30),
	relr_dm varchar(30),
	constraint relr_un
		unique (relr_diag_id, relr_mode_id),
	check (relr_end_connector IN ('1','M')),
	check (relr_start_connector IN ('1','M')),
	constraint relr_eab_chk
		check (relr_endtext_distance BETWEEN 1 AND 9999),
	constraint relr_eb_chk
		check (relr_endtext_width BETWEEN 1 AND 9999),
	constraint relr_eh_chk
		check (relr_endtext_height BETWEEN 1 AND 9999),
	constraint relr_ek_chk
		check (relr_endedge IN ('N','E','S','W')),
	constraint relr_ep_chk
		check (relr_endposition BETWEEN 0.0 AND 100.0),
	constraint relr_ewi_chk
		check (relr_endtext_angle BETWEEN -3.1415926535898 AND 3.141592653589793),
	constraint relr_ex_chk
		check (relr_endtext_x BETWEEN 0 AND 999999),
	constraint relr_ey_chk
		check (relr_endtext_y BETWEEN 0 AND 999999),
	constraint relr_ldk_chk
		check (relr_lineopacity BETWEEN 0 AND 100),
	constraint relr_lf_chk
		check (length(relr_linecolor)= 6),
	constraint relr_sf_chk
		check (length(relr_fontcolor)= 6),
	constraint relr_sg_chk
		check (relr_fontsize BETWEEN 1 AND 999),
	constraint relr_stab_chk
		check (relr_starttext_distance BETWEEN 1 AND 9999),
	constraint relr_stb_chk
		check (relr_starttext_width BETWEEN 1 AND 9999),
	constraint relr_sth_chk
		check (relr_starttext_height BETWEEN 1 AND 9999),
	constraint relr_stk_chk
		check (relr_startedge IN ('N','E','S','W')),
	constraint relr_stp_chk
		check (relr_startposition BETWEEN 0.0 AND 100.0),
	constraint relr_stwi_chk
		check (relr_starttext_angle BETWEEN -3.1415926535898 AND 3.141592653589793),
	constraint relr_stx_chk
		check (relr_starttext_x BETWEEN 0 AND 999999),
	constraint relr_sty_chk
		check (relr_starttext_y BETWEEN 0 AND 999999)
);

create table linesegments
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
	lise_uc varchar(30) not null,
	lise_dc varchar(30) not null,
	lise_um varchar(30),
	lise_dm varchar(30),
	constraint lise__un
		unique (lise_relr_id, lise_seq),
	constraint ck_lise_linetype
		check (lise_linetype IN('DADO','DASHED','DOTTED','SOLID')),
	constraint lise_angle_chk
			check (lise_angle BETWEEN -3.1415926535898 AND 3.141592653589793),
    CONSTRAINT ck_lise_x CHECK(lise_x BETWEEN 0 AND 999999) ,
	constraint ck_lise_y check (lise_y BETWEEN 0 AND 999999)
);

create table tables
(
	tabl_id integer
		primary key autoincrement
		constraint TABL_MODE_FK
			references MODELELEMENT (mode_id)
		on delete cascade,
	tabl_name varchar(60) not null,
	tabl_intf_id integer not null
		references interfaces (intf_ID),
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
		unique (tabl_intf_id, tabl_name)
);

create table columns
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
	colu_doma_id integer not null
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

create table colu_attr_map
(
	coam_id integer
		primary key autoincrement,
	coam_seq integer not null,
	coam_direction varchar(7) not null,
	coam_transf_rule varchar(4000),
	coam_triggertype varchar(10),
	coam_triggerperiod integer,
	coam_colu_id integer not null
		references columns (colu_id)
			on delete cascade,
	coam_attr_id integer not null
		constraint coam_attr_fk
			references ATTRIBUTES (attr_id)
				on delete cascade,
	coam_enti_id integer
		constraint coam_enti_fk
			references entities (enti_id)
				on delete cascade, 
	constraint coam_un
		unique (coam_direction, coam_colu_id, coam_attr_id, coam_seq),
	check (coam_direction in ('INBOUND', 'OUTBOUND')),
	check (coam_seq > 0),
	check (coam_triggertype in ('MANUELL', 'PERIODE', 'ZPKT'))
);


create table tabl_enti_maps
(
	tema_id integer
		primary key autoincrement,
	tema_tabl_id integer not null
		references tables (tabl_id) on delete  cascade ,
	tema_enti_id integer
		constraint tema_enti_fk
			references ENTITIES (enti_id) on delete cascade ,
	tema_rela_id integer
		constraint tema_rela_fk
			references RELATIONS (rela_id) on delete cascade ,
	constraint tema_unenti
		unique (tema_tabl_id, tema_enti_id),
	constraint tema_unrela
		unique (tema_tabl_id, tema_rela_id),
	constraint tema_ck
		check ((tema_enti_id is not null and tema_rela_id is null )
      	        		  or (tema_enti_id is null and tema_rela_id is not null))
);

create table business_rules
    (
     buru_id integer not null primary key autoincrement
    		constraint buru_mode_fk
			references modelelement (mode_id)
		on delete cascade,
     buru_name varchar (60) not null constraint buru_un unique,
     buru_rule varchar (4000) not null ,
     buru_descr varchar (4000) null ,
     buru_impact varchar (4000) null ,
     buru_type varchar (10) not null constraint ck__business___buru___1293bd5e check ( buru_type='TRIGGER' or buru_type='CHECK' or buru_type='CALC' ) ,
     buru_level varchar (10) not null constraint ck__business___buru___1387e197 check ( buru_level='TUPL' or buru_level='ENTI' or buru_level='DB' or buru_level='ATTR' ) ,
     buru_errormsg varchar (100) ,
     buru_uc varchar (30) not null ,
     buru_dc varchar(30) not null ,
     buru_um varchar (30) null ,
     buru_dm varchar(30) null
    );

create table businessrule_elements
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

create table element_ui
    (
     elui_id integer not null primary key ,
     elui_melt_id numeric (10) null
            references modelelem_type (melt_id) on delete cascade ,
     elui_enca_id numeric (10) null
            references entity_categories (enca_id) on delete cascade ,
     elui_width numeric (4) null ,
     elui_height numeric (4) null ,
     elui_opacity numeric (3) null default (100) constraint ck__elementre__eler___3cf40b7e check ( elui_opacity>=0 and elui_opacity<=100 ) ,
     elui_color varchar (6) null default '000000' constraint ck__elementre__eler___3edc53f0 check ( length(elui_color) = 6 ) ,
     elui_marginwidth numeric (3,1) null default (1) ,
     elui_marginopacity numeric (3) null default (100) constraint ck__elementre__eler___41b8c09b check ( elui_marginopacity>=0 and elui_marginopacity<=100 ) ,
     elui_margincolor varchar (6) null default '000000' constraint ck__elementre__eler___43a1090d check ( length(elui_margincolor) = 6 ) ,
     elui_fontsize numeric (3) null constraint ck__elementre__eler___44952d46 check ( elui_fontsize>=1 and elui_fontsize<=999 ) ,
     elui_fontcolor varchar (6) null default '000000' constraint ck__elementre__eler___467d75b8 check ( length(elui_fontcolor) = 6 )
    ,constraint fkarc_3 check (
        (  (elui_melt_id is not null) and
         (elui_enca_id is null) ) or
        (  (elui_enca_id is not null) and
         (elui_melt_id is null) )
        )
	    ,constraint elui_uxk_melt unique  (elui_melt_id)
	    ,constraint elui_uk_enca unique  (elui_enca_id)
    );

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

create view superenti as
        with rel as (select rela_type
               , case
                     when rela_mandatory_to_from = 'TRUE' then rela_enti_id_from
                     else rela_enti_id_to end as rela_superenti_id
               , case
                     when rela_mandatory_from_to = 'TRUE' then rela_enti_id_from
                     else rela_enti_id_to end as rela_subenti_id
                 from relations
                where rela_type = 'ISAR'
                )
    select rela_type,superentity.enti_id as superenti_id, superentity.enti_name as super_enti_name
        ,subentity.enti_id as subenti_id, subentity.enti_name as sub_enti_name
          from entities superentity
            join arcs on arcs_enti_id = superentity.enti_id
            join relations
                  on  ((rela_arcs_id_from  = arcs_id and rela_enti_id_from = superentity.enti_id)
                   or (rela_arcs_id_to  = arcs_id and rela_enti_id_to = superentity.enti_id))
                     and rela_type =  'ISAS'
           left  join entities subentity on  (subentity.enti_id =  rela_enti_id_to and rela_arcs_id_from = arcs_id )
                or (subentity.enti_id =  rela_enti_id_from and rela_arcs_id_to = arcs_id )
    union all
        select rela_type,superentity.enti_id as superenti_id, superentity.enti_name as super_enti_name
        ,subentity.enti_id as subenti_id, subentity.enti_name as sub_enti_name
          from entities superentity
          join rel on rela_superenti_id = superentity.enti_id
        join entities subentity on subentity.enti_id = rela_subenti_id;




create view dbversion as select '2.0' as version, '2022-07-18 10:00' as installedtime;
	-- sql-server: create view  dbversion as select '1.0' as version, current_timestamp as installedtime
	-- postgres: create view  dbversion as select '1.0' as version, current_timestamp as installedtime
