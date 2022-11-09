-- Upgrade db to version 1.9

-- in case of violations during upgrade, switch constraints off and on again
PRAGMA ignore_check_constraints = ON;

alter table colu_attr_map 
add coam_enti_id integer
	constraint coam_enti_fk
		references entities (enti_id)
			on delete cascade;

drop view dbversion;
create view dbversion as select '1.9.1' as version, '2022-06-01 14:30' as installedtime;

PRAGMA ignore_check_constraints = OFF;

