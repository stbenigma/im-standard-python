-- Upgrade db to version 1.3
drop view dbversion;
create view dbversion as select '1.3' as version, datetime() as installedtime;
