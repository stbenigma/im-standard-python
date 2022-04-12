from pathlib import Path

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
def deploy(c):
    print(f"Deploying generator")
    with c.cd(PROJECT_ROOT):
        c.run(f"python {SOURCE_FOLDER}/tools/deploy.py")


@task(pre=[deploy], aliases=['gen', 'generate'])
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
