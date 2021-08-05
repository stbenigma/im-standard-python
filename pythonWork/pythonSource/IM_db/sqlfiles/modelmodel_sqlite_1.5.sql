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

drop view dbversion;
create view dbversion as select '1.5' as version, datetime() as installedtime;
