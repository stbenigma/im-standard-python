-- Upgrade db to version 1.6

create table relationreps_tmp
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
PRAGMA ignore_check_constraints = 0;
update relationreps
	set relr_endedge = 'E'
	where relr_endedge = 'O';
update relationreps
	set relr_startedge = 'E'
	where relr_startedge = 'O';	
PRAGMA ignore_check_constraints = 1;
insert into relationreps_tmp select * from relationreps;
drop table relationreps;
alter table relationreps_tmp rename to relationreps;


drop view dbversion;
create view dbversion as select '1.6' as version, datetime() as installedtime;
