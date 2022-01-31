-- Upgrade db to version 1.6.1

alter table entities add column
    enti_underlay_enti_id numeric (10) null
        references entities (enti_id);
PRAGMA ignore_check_constraints = 0;
PRAGMA ignore_check_constraints = 1;

drop view dbversion;
create view dbversion as select '1.6.1' as version, datetime() as installedtime;
