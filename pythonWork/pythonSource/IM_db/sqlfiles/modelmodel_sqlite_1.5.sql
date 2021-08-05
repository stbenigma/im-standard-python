-- Upgrade db to version 1.5
drop view dbversion;
create view dbversion as select '1.5' as version, datetime() as installedtime;
