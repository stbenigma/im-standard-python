Concept for DB-Model installation

SQLITE

Versions (referred to as <version> below) of the database structure are in the form:
	major.minor (e.g. 1.5)

Versions of databasestructure strictly follow each other (in the sequence of ordered (string) <version> ).
This means version upgrades can and must be applied in the order of ordered file-names.

Every sql-script changing the database structure contains a version-View
	create view dbversion as select '<version>' as version, datetime() as installedtime;
	
If the script is applied to a existing DB we need to drop the view beforehand
	drop view dbversion

The current SQL-script for a complete database structure is in the file
	modelmode_sqlite.sql
	
All version upgrades (upgrades to <version>) are in the file.
	modelmodel_sqlite_<version>.sql 
	including: 
		structural preparation of data migration
		changes to DB structure
		migration of existing data 
		cleanup of data migration structures)
		creatig new version-View

For data migration which cannot be done with SQL alone, we have to add a concept of python code inclusion.

Algorithm for upgrades:
	get actual version of DB
	apply all modelmode_sqlite_<version>.sql files with filename greater than modelmode_sqlite_<acutalversion> in the order of their filenames.
	stop a soon as the applied version equals the expected version in the tool.