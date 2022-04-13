#
# Tasks for the invoke 'https://www.pyinvoke.org/ library
# We use this instead of a Make / Scons / ... build automation tool
#

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
TEST_MODEL = SOURCE_FOLDER / 'testenvironment' / 'testmodels' / 'riddle'
TEST_MODEL_DB = TEST_MODEL / 'DB' / 'riddle.db'


@task
def bootstrap(c):
    c.run('conda env update --file conda-base-environment.yaml')
    c.run('pip run ')


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
    print(f"Deprecated, use 'package' task instead")
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
              profile=False):
    if model is None:
        model = TEST_MODEL / 'IM'
        if languages is None:
            languages = 'en'
    else:
        model = Path(model)

    if not model.is_absolute():
        abs_rel = Path(PROJECT_ROOT, model)
        if not abs_rel.is_dir():
            model = model.relative_to(PROJECT_ROOT).resolve()
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

    command = f"python dist/generator.py --model='{model.resolve()}' {' '.join(optargs)}"
    with c.cd(PROJECT_ROOT):
        print(f"Starting generator with: {command} in {PROJECT_ROOT}")
        c.run(command)

    if profile:
        print(f"⏱⏱⏱ Profile results in log/ ⏱⏱⏱")
        print(f"snakeviz log/generator-lastest-fillmergedb.prof")


@task
def dbversion(c, model=None):
    if model is None:
        model = TEST_MODEL / 'DB' / 'riddle.db'
    dbfile = Path(model).resolve()
    if not dbfile.is_file():
        print(f"{dbfile} is not file")
        exit(1)
    c.run(f"""sqlite3 {dbfile} 'select * from dbversion'""")


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
        if '/Users/' in lower_content_string:
            raise ValueError(f"/Users/ found in content")
    except UnicodeDecodeError:
        pass
    pass