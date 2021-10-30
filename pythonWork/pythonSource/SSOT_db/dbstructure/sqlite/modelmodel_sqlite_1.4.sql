-- Upgrade db to version 1.4
drop view dbversion;
create view dbversion as select '1.4' as version, datetime() as installedtime;
