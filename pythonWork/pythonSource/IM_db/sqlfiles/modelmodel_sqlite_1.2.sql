-- Upgrade db to version 1.2
drop view dbversion;
create view dbversion as select '1.2' as version, datetime() as installedtime;
