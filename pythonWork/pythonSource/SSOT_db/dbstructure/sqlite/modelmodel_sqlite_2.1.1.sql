-- Upgrade db to version 2.1.1

-- in case of violations during upgrade, switch constraints off and on again
PRAGMA ignore_check_constraints = ON;

INSERT INTO modelelem_type (melt_id, melt_shortname, melt_name, melt_uc, melt_dc) VALUES (20, 'DATM', 'Datamodel', 'SYS', '2023-12-29');
INSERT INTO modelelem_type (melt_id, melt_shortname, melt_name, melt_uc, melt_dc) VALUES (21, 'MAPS', 'Mapping', 'SYS', '2023-12-29');
INSERT INTO modelelem_type (melt_id, melt_shortname, melt_name, melt_uc, melt_dc) VALUES (22, 'SYST', 'System', 'SYS', '2023-12-29');
UPDATE modelelem_type SET melt_name = 'Datatype', melt_um = 'SYS', melt_dc = '2023-12-29' WHERE melt_shortname = 'DATY';


drop view if exists dbversion;
create view dbversion as select '2.1.1' as version, '2024-01-04 10:00' as installedtime;

PRAGMA ignore_check_constraints = OFF;

