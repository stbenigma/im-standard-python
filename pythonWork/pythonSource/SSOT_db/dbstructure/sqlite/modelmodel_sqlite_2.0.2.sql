-- Upgrade db to version 2.0.2

-- in case of violations during upgrade, switch constraints off and on again
PRAGMA ignore_check_constraints = ON;

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
 or ( doma_bin_contenttype is null and doma_bin_stfo_id is null and doma_dat_granularity is null and doma_dat_maxvalue is null and doma_dat_minvalue is null and doma_txt_syntaxrule is null and doma_txt_maxlng is null)),
	constraint doma_exdep6
		check (doma_type != 'TXT'
 or ( doma_bin_contenttype is null and doma_bin_stfo_id is null and doma_num_fract_digits is null and doma_num_maxvalue is null and doma_num_minvalue is null and doma_num_phyu_id is null and doma_num_round_value is null and doma_num_total_digits is null and doma_dat_granularity is null and doma_dat_maxvalue is null and doma_dat_minvalue is null))
,constraint doma_num_1 check ( doma_num_minvalue is null 
			or doma_num_maxvalue is null or doma_num_minvalue <= doma_num_maxvalue ) 
,constraint doma_num_2 check ( doma_num_fract_digits is null or doma_num_total_digits is null or doma_num_fract_digits < doma_num_total_digits) 
);
	
insert into domains_temp select * from domains;
drop table domains;
alter table domains_temp rename to domains;


drop view dbversion;
create view dbversion as select '2.0.2' as version, '2022-10-24 10:00' as installedtime;

PRAGMA ignore_check_constraints = OFF;

