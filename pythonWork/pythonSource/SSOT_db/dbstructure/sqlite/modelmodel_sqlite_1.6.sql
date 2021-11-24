-- Upgrade db to version 1.6
drop view dbversion;
create view dbversion as select '1.6' as version, datetime() as installedtime;
