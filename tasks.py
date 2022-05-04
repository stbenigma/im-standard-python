#
# Tasks for the invoke 'https://www.pyinvoke.org/ library
# We use this instead of a Make / Scons / ... build automation tool
#
import pathlib
from pathlib import Path
import sys
import zipfile as zlib

try:
    from invoke import task
except ModuleNotFoundError:
    print("invoke module not found. Install using 'conda install invoke'")
    exit(-1)

PROJECT_ROOT = Path(__file__).parent.resolve()
SOURCE_FOLDER = PROJECT_ROOT / 'pythonWork' / 'pythonSource'
TESTMODELS_BASE = SOURCE_FOLDER / 'testenvironment' / 'testmodels'
TEST_MODEL = TESTMODELS_BASE / 'riddle'
TEST_MODEL_DB = TEST_MODEL / 'DB' / 'riddle.db'
INTEGRATION_TEST_FOLDER =  PROJECT_ROOT / 'testdata'


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
def dbversion(c, model=None, full=False):
    if full:
        c.run(f"""echo expected  `less {PROJECT_ROOT / 'pythonWork/pythonSource/SSOT_infra/versions.json'} | grep 'DBVERSION'` """)
    if model is None:
        model = 'riddle'
    if model in ('crmTest','riddle','testmodel-1','testmodel-2'):
        model = TESTMODELS_BASE / model / 'DB' / f"{model}.db"
    dbfile = Path(model).resolve()
    if not dbfile.is_file():
        print(f"{dbfile} is not file")
        exit(1)
    c.run(f"""sqlite3 {dbfile} 'select * from dbversion'""")

@task
def upgradedb(c, model=None):
    def upgrade1db(model):
        if model in ('crmTest', 'riddle', 'testmodel-1', 'testmodel-2'):
            modelpath = TESTMODELS_BASE / model / 'DB' / f"{model}.db"
        else:
            modelpath = Path(model) #assume it is a modeldbfilepath
            model = modelpath.stem
        dbfile = modelpath.resolve()
        if not dbfile.is_file():
            print(f"{dbfile} is not file")
            exit(1)
        with c.cd(PROJECT_ROOT):
            from SSOT_db import createDB
            createDB(pupgrade=True, pdestination=dbfile,pmodelname=model)
            #c.run(f"""python {SOURCE_FOLDER}/SSOT_db/createDB.py -u -d {dbfile}""")
        return

    load_tools_library()
    if model is None:
        for model in ('crmTest','riddle','testmodel-1','testmodel-2'):
            upgrade1db(model)
    else:
        upgrade1db(model)



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
