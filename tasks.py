#
# Tasks for the invoke 'https://www.pyinvoke.org/ library
# We use this instead of a Make / Scons / ... build automation tool
#
import json
import pathlib
import shutil
from contextlib import closing
from pathlib import Path
import sys
import zipfile as zlib

import logging
import os
from logging import handlers
from datetime import datetime

try:
    from invoke import task
except ModuleNotFoundError:
    print("Python module 'invoke' not found. Install using 'conda install invoke'")
    print("See: https://www.pyinvoke.org/")
    exit(-1)

PROJECT_ROOT = Path(__file__).parent.resolve()
SOURCE_FOLDER = PROJECT_ROOT / 'pythonWork' / 'pythonSource'
TESTMODELS_BASE = SOURCE_FOLDER / 'testenvironment' / 'testmodels'
TEST_MODEL = TESTMODELS_BASE / 'riddle'
TEST_MODEL_DB = TEST_MODEL / 'DB' / 'riddle.db'
INTEGRATION_TEST_FOLDER = PROJECT_ROOT / 'testdata'


def initialize_logging(start_message: str = None):
    stamp = datetime.now()
    run_stamp = stamp.strftime("%Y-%m-%d_%H-%M-%S")

    os.makedirs('log', exist_ok=True)
    logfile = f'log/invoke-{run_stamp}.log'
    formatter = logging.Formatter("%(asctime)s [%(threadName)s] - %(name)s - %(levelname)s - %(message)s")

    file_handler = handlers.RotatingFileHandler(logfile, maxBytes=(1024 * 1024 * 20), backupCount=10)
    file_handler.setFormatter(formatter)

    console_log_handler = logging.StreamHandler()
    console_formatter = logging.Formatter("%(levelname)s - %(message)s")
    console_log_handler.setFormatter(console_formatter)


    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    root_logger.addHandler(console_log_handler)
    root_logger.addHandler(file_handler)

    console_log_handler.setLevel(logging.INFO)
    file_handler.setLevel(logging.DEBUG)

    if start_message is not None:
        root_logger.info(start_message)


def load_tools_library():
    sys.path.append(f"{SOURCE_FOLDER}")
    import SSOT_infra
    ver = SSOT_infra.__version__
    return ver


@task
def update_infrastructure(c):
    c.run('conda env update --file conda-base-environment.yaml')


@task
def translate(c):
    locales = Path(SOURCE_FOLDER, 'SSOT_infra', 'locales')
    assert locales.is_dir()
    for po in locales.rglob('**/*.po'):
        dest = po.with_suffix('.mo')
        c.run(f"msgfmt -v -o {dest} {po}")


@task(translate)
def package(c):
    print(f"Deploying generator")
    sys.path.append(f"{SOURCE_FOLDER}")
    from tools import deploy
    argv = []
    try:
        idx = sys.argv.index('--')
        argv.extend(sys.argv[idx:])
    except ValueError:
        pass
    with c.cd(PROJECT_ROOT):
        print(f"Running in {pathlib.Path.cwd()}")
        c.package = deploy.main(basefolder=PROJECT_ROOT, argv=argv)


@task(pre=[package], aliases=['verify', 'check'])
def verify_package(c):
    assert c.package is not None
    print(f"Verifying package content of {c.package}")
    with zlib.ZipFile(c.package, 'r') as src:
        for element in src.filelist:
            print(f"Scanning {element.filename} ({element.file_size})")
            with src.open(element, 'r') as content:
                try:
                    verify_content(content)
                except ValueError as exc:
                    raise ValueError(f"Found stopword in file {element.filename}") from exc


@task(pre=[verify_package])
def deploy(c):
    print(f"Deprecated tas {c}, use 'package' task instead")
    pass


@task(pre=[package], aliases=['gen', 'generate'])
def generator(c, model=None,
              languages=None,
              skip_odm=False,
              all=False,
              skip_web=False,
              confluence=False,
              sharepoint=False,
              sparx_ea=False,
              link_udpr=None,
              profile=False,
              version=False,
              verbose=False,
              spod_only=False,
              ):
    if model is None:
        model = TEST_MODEL / 'IM'
        if languages is None:
            languages = 'en'
    else:
        model = Path(model)

    if not model.is_absolute():
        abs_rel = Path(PROJECT_ROOT, model)
        if not abs_rel.is_dir():
            cwd = pathlib.Path.cwd()
            model = cwd / model
        else:
            model = abs_rel

    optargs = []
    if skip_odm:
        optargs.append("--skip-odm")
    if skip_web:
        optargs.append("--skip-web")

    # override all skip options if --all is defined
    if all:
        optargs.clear()

    if all or confluence:
        optargs.append("--confluence")
    if all or sharepoint:
        optargs.append("--sharepoint")
    if all or sparx_ea:
        optargs.append("--sparx-ea")

    if languages is not None:
        optargs.append(f"--languages='{languages}'")

    if link_udpr is not None:
        optargs.append("--link-udpr=" + link_udpr)

    if profile:
        print("⏱⏱⏱ Running in profiler mode: This might take some time  ⏱⏱⏱")
        optargs.append("--profile")

    if version:
        optargs.append("--version")

    if verbose:
        optargs.append("--verbose")

    if spod_only:
            optargs.append("--spod-only")

    command = f"python dist/generator.py --model='{model.resolve()}' {' '.join(optargs)}"
    with c.cd(PROJECT_ROOT):
        print(f"Starting generator with: {command} in {PROJECT_ROOT}")
        c.run(command)

    if profile:
        print(f"⏱⏱⏱ Profile results in log/ ⏱⏱⏱")
        print(f"snakeviz log/generator-lastest-fillmergedb.prof")


@task
def dbversion(c, model=None, full=False, db=None):
    if full:
        c.run(
            f"""echo expected `less {PROJECT_ROOT / 'pythonWork/pythonSource/SSOT_infra/versions.json'} | grep 'DBVERSION'` """)
    if model is None:
        model = 'riddle'
    if model in ('crmTest', 'riddle', 'testmodel-1', 'testmodel-2'):
        model = TESTMODELS_BASE / model / 'DB' / f"{model}.db"
    if db is not None:
        model = db
    dbfile = Path(model).resolve()
    if not dbfile.is_file():
        print(f"{dbfile} is not file")
        exit(1)
    c.run(f"""sqlite3 {dbfile} 'select * from dbversion'""")

    load_tools_library()
    from SSOT_db.SQL_INFRA.dbConnect import openDB

    with closing(openDB(dbfile)) as connection:
        print(f"Entities: {count(connection, 'entities')}")
        print(f"Attributes: {count(connection, 'attributes')}")
        print(f"Systems: {count(connection, 'interfaces')}")
        print(f"Tables: {count(connection, 'tables')}")
        print(f"Columns: {count(connection, 'columns')}")



@task
def upgradedb(c, model=None):
    def upgrade1db(model):
        if model in ('crmTest', 'riddle', 'testmodel-1', 'testmodel-2'):
            modelpath = TESTMODELS_BASE / model / 'DB' / f"{model}.db"
        else:
            modelpath = Path(model)  # assume it is a modeldbfilepath
            model = modelpath.stem
        dbfile = modelpath.resolve()
        if not dbfile.is_file():
            print(f"{dbfile} is not file")
            exit(1)
        with c.cd(PROJECT_ROOT):
            from SSOT_db import createDB
            path = createDB(pupgrade=True, pdestination=dbfile, pmodelname=model)
            # c.run(f"""python {SOURCE_FOLDER}/SSOT_db/createDB.py -u -d {dbfile}""")
            return dbfile

    print(load_tools_library())
    if model is None:
        for model in ('crmTest', 'riddle', 'testmodel-1', 'testmodel-2'):
            upgrade1db(model)
    else:
        db_file = upgrade1db(model)
        from SSOT_db.IM_JSON import JSModel, sql2json
        from SSOT_db.SQL_INFRA.dbConnect import openDB, closeDB
        with closing(openDB(db_file)) as conn:
            loadedjson = JSModel(pmodel=sql2json(pdbname=str(db_file)))
            json_file = loadedjson.printmodel(pfilepath=str(db_file.parent), pfilename=db_file.stem)
            closeDB()
            json = loadedjson.jsmodel
            print(f"\x1b[32mSucessfully\x1b[39m upgraded database {db_file}" \
                  f" and JSON {json_file} to version {json['_imprint_'].get('Modelversion', '?.?')}" \
                  f" git revision: {json['_imprint_'].get('git-revision', '?????')}")


@task(aliases=['but'])
def bootstrap_unit_tests(c):
    required_models = [
        TESTMODELS_BASE / 'crmTest',
        TESTMODELS_BASE / 'riddle',
        TESTMODELS_BASE / 'testmodel-1',
        TESTMODELS_BASE / 'testmodel-2',
    ]

    # more generic:  for hit in glob.glob(f"testdata/**/IM", recursive=True):
    for hit in required_models:
        candidate = Path(hit)
        if candidate.is_dir():
            print(f"Generating SPOD for {hit}")
            c.run(f"inv generator --spod-only -m {candidate / 'IM'}")


@task
def checkout_refmodels(c):
    base = INTEGRATION_TEST_FOLDER
    if not base.is_dir():
        print(f"Checking out refmodels (https://github.com/foryouandyourcustomers/fyyccim-refmodels)")
        c.run(f"git clone --progress --depth 1 git@github.com:foryouandyourcustomers/fyyccim-refmodels.git {str(base)}")


@task(aliases=['bit'], pre=[checkout_refmodels])
def bootstrap_integration_tests(c):
    required_models = [
        'testdata/fyyccim-refmodels/CRM/IM',
        'testdata/fyyccim-refmodels/PIM/IM',
    ]

    # more generic:  for hit in glob.glob(f"testdata/**/IM", recursive=True):
    for hit in required_models:
        candidate = Path(hit)
        if candidate.is_dir():
            print(f"Generating SPOD for {hit}")
            c.run(f"inv generator --spod-only -m {candidate}")


@task(aliases=['filldb'],
      help={
          'source': "JSON source [mandatory]",
          'srcname': "Name of the source",
          'output': "Path of the destination file. Source path with .db extension if undefined",
          'nomerge': "Overwrite current database"})
def json2db(c, source, srcname, output=None, nomerge=False, verbose=True, dry=False):
    """
    Fill database form SPOD (JSON source)
    @:param dry Dry run
    """
    initialize_logging("json2db")
    load_tools_library()
    src_path = Path(source)

    if not src_path.is_file():
        raise Exception(f"Source '{src_path.resolve()}' is not a file")

    if output is None:
        out_path = src_path.with_suffix('.db')
    else:
        out_path = Path(output)

    with open(src_path, 'r') as src:
        spod = json.load(src)

    print(f"Successfully loaded model {spod['model']['name']} {spod['_imprint_'].get('git-revision')}")

    from SSOT_db.SQL_INFRA import dbConnect
    from SSOT_infra import parameters
    from SSOT_db.IM_JSON import JSModel
    from SSOT_db.createDB import createnewDB
    from LOAD_MODELS.LOAD_INFRA import mergedbs

    revision = spod['_imprint_'].get('git-revision', parameters.read_git_description(src_path.parent))
    print(f"Created SPOD for git revision {revision}")

    parameters.initparam(str(SOURCE_FOLDER), pmodelname=src_path.stem)
    # parameters.sqlpath(str(SOURCE_FOLDER / 'SSOT_db' / 'dbstructure'))

    # prepare target
    archive = src_path.parent / '.archive'
    archive.mkdir(exist_ok=True)

    if out_path.is_file():
        backup = archive / out_path.name
        index = 1
        while backup.is_file():
            backup = archive / f"{out_path.name}.{index}"
            index += 1
        print(f"Moving current database to archive '{backup}'")
        shutil.copy(out_path, backup)

    if nomerge:
        out_path.unlink(missing_ok=True)

    if out_path.is_file():
        print(f"Updating database {out_path}")
        database = dbConnect.openDB(str(out_path))
    else:
        print(f"Creating database {out_path}")
        database = createnewDB(str(out_path))

    with closing(database) as conn:
        dbConnect.write_git_reversion(revision, conn)
        model = JSModel(spod)
        mergedbs.mergejs2db(pdbfile=str(out_path.resolve()), pmodel=model, psrcname=srcname,
                            pverbose=verbose, pdryrun=dry, pkeepids=nomerge)

        print(f"Entities: {count(database, 'entities')}")
        print(f"Attributes: {count(database, 'attributes')}")
        print(f"Systems: {count(database, 'interfaces')}")
        print(f"Tables: {count(database, 'tables')}")
        print(f"Columns: {count(database, 'columns')}")

    print(f"\x1b[32mSucessfully\x1b[39m created database {out_path} from json SPOD {src_path}")


def count(connection, table: str) -> int:
    with closing(connection.cursor()) as cursor:
        cursor.execute(f"SELECT count(*) FROM [{table}]")
        curr_table = cursor.fetchall()
        return curr_table[0][0]

@task(help={
    'source': "SPOD database [mandatory]",
    'output': "Path of the destination json. Source path with .json extension if undefined"
})
def db2json(c, source, output=None):
    initialize_logging("db2json")
    load_tools_library()
    src_path = Path(source)

    if source is None:
        raise ValueError("no source database defined")

    if not src_path.is_file():
        raise Exception(f"Source '{src_path.resolve()}' is not a file")

    if output is None:
        out_path = src_path.with_suffix('.json')
    else:
        out_path = Path(output)

    from SSOT_db.SQL_INFRA import dbConnect
    from SSOT_infra import parameters
    from SSOT_db.IM_JSON import JSModel

    parameters.initparam(str(SOURCE_FOLDER), pmodelname=src_path.stem)
    # parameters.sqlpath(str(SOURCE_FOLDER / 'SSOT_db' / 'dbstructure'))

    # prepare target
    archive = src_path.parent / '.archive'
    archive.mkdir(exist_ok=True)

    if out_path.is_file():
        backup = archive / out_path.name
        index = 1
        while backup.is_file():
            backup = archive / f"{out_path.name}.{index}"
            index += 1
        print(f"Moving current json to archive '{backup}'")
        shutil.copy(out_path, backup)

    from SSOT_db.IM_JSON import sql2json
    with closing(dbConnect.openDB(src_path)):
        model = JSModel(sql2json(pdbname=dbConnect.getDBname()))
        git_revision = dbConnect.read_git_revision(dbConnect.getdbcon())
        revision = model.jsmodel['_imprint_']['git-revision'] = git_revision
        print(f"Writing SPOD for git revision {revision} to {out_path}")
        model.write_json(out_path)
    print("Summary:\n" + json.dumps(model._repr_json_(), indent=4))
    print(f"\x1b[32mSucessfully\x1b[39m created {out_path} from SPOD {src_path}")


def verify_content(fh):
    data = fh.read()
    try:
        lower_content_string = data.decode().lower()
        if 'geberit' in lower_content_string:
            raise ValueError(f"geberit found in content")
        if 'sika' in lower_content_string:
            raise ValueError(f"sika found in content")
        if 'bossard' in lower_content_string:
            raise ValueError(f"bossard found in content")
        if 'ktlu' in lower_content_string:
            raise ValueError(f"bossard found in content")
        if 'bosch' in lower_content_string:
            raise ValueError(f"bosch found in content")
        if 'komax' in lower_content_string:
            raise ValueError(f"komax found in content")
        if '/Users/' in lower_content_string:
            raise ValueError(f"/Users/ found in content")
    except UnicodeDecodeError:
        pass
    pass


@task
def createtestmodeldbs(c):
    def fillone(model):
        """init module with regenerating the testmodels db and jsons"""
        try:
            integration.Testmodel(model).initDB(palways=True)
        except:
            print(f"could not fill {model}")

    load_tools_library()
    with c.cd(PROJECT_ROOT):
        from SSOT_infra.tests import integration

        fillone(integration.TESTMODEL1)
        fillone(integration.TESTMODEL2)
        fillone(integration.CRMTEST)
        fillone(integration.RIDDLE)


@task
def unittest(c):
    """Run unittests tests using pytest"""
    import pytest as pt
    pt.main(['-m', 'not integration'])


@task
def integrationtest(c):
    """Run integration tests using pytest"""
    import pytest as pt
    pt.main(['-m', 'integration'])


@task(pre=[unittest, integrationtest])
def test(c):
    """Virtual target running all tests"""
    pass
