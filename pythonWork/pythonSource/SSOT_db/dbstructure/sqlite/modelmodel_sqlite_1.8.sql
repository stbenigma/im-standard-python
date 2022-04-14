-- Upgrade db to version 1.8

-- in case of violations during upgrade, switch constraints off and on again
--PRAGMA ignore_check_constraints = 0;
--PRAGMA ignore_check_constraints = 1;

alter table businessrule_elements add 
     bure_role VARCHAR (4) constraint ck__businessr__bure___10216507  check ( bure_role in ('AFCT', 'REF'));


drop view dbversion;
create view dbversion as select '1.8' as version, datetime() as installedtime;
