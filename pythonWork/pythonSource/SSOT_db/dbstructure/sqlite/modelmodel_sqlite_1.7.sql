-- Upgrade db to version 1.7

-- in case of violations during upgrade, switch constraints off and on again
--PRAGMA ignore_check_constraints = 0;
--PRAGMA ignore_check_constraints = 1;

create table modelelement_tmp
(
	mode_id integer not null
		primary key autoincrement,
	mode_type varchar(4) not null,
	mode_melt_id integer not null
		references modelelem_type (melt_id),
    mode_min_zoom_level numeric(1) null check ( mode_min_zoom_level between 0 and 4 ) ,
    mode_max_zoom_level numeric(1)  null check ( mode_max_zoom_level between 0 and 4 ) ,
	mode_publ_status varchar (5) null check ( mode_publ_status in ('DRAFT', 'GTOP', 'PUBL') ) 
	check (mode_type in ("ARCS", "ATTR", "BURU", "COLU", "DOMA", "ENTI"
                            , "INTF", "ORGU", "RELA", "SYNO", "TABL","DOCU"
							,"KEYS","DATY","DGRM","DIAG","EXPL"))
);

insert into modelelement_tmp (mode_id,mode_type,mode_melt_id,mode_min_zoom_level,mode_max_zoom_level,mode_publ_status)
	select mode_id,   mode_type,   mode_melt_id
	      ,mode_min_zoom_level,   mode_max_zoom_level
		  ,case mode_dev_status
		  		when "DEV" then "DRAFT"
				when "TEST" then "GTOP"
				when "REL" then "PUBL"
				else NULL
			end mode_publ_status
		  	from modelelement;
drop table modelelement;
alter table modelelement_tmp rename to modelelement;

drop view dbversion;
create view dbversion as select '1.7' as version, datetime() as installedtime;
