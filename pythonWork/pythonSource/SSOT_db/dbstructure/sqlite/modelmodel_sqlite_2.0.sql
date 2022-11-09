-- Upgrade db to version 2.0

-- in case of violations during upgrade, switch constraints off and on again
PRAGMA ignore_check_constraints = ON;

create table keys_temp
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
insert into keys_temp  (keys_id ,
	keys_name, 	keys_enti_id ,keys_uc,
	keys_dc ,
	keys_um ,
	keys_dm)
	select keys_id ,
	keys_name, 	keys_enti_id ,keys_uc,
	keys_dc ,
	keys_um ,
	keys_dm from keys;

drop table keys;
alter table keys_temp rename to keys;

drop view dbversion;
create view dbversion as select '2.0' as version, '2022-07-18 10:00' as installedtime;

PRAGMA ignore_check_constraints = OFF;

