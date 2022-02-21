from pathlib import Path

try:
    from invoke import task
except ModuleNotFoundError:
    print("invoke module not found. Install using 'conda install invoke'")
    exit(-1)

SOURCE_FOLDER = "pythonWork/pythonSource"
TEST_MODEL = "pythonWork/pythonSource/testenvironment/testmodels/riddle/IM"


@task
def translate(c):
    locales = Path(SOURCE_FOLDER, 'SSOT_infra', 'locales')
    assert locales.is_dir()
    for po in locales.rglob('**/*.po'):
        dest = po.with_suffix('.mo')
        c.run(f"msgfmt -v -o {dest} {po}")


@task(translate)
def deploy(c):
    c.run(f"python {SOURCE_FOLDER}/tools/deploy.py")


@task(deploy)
def generator(c, model=TEST_MODEL, languages=None, skip_odm=False,
              all=False, skip_web=False,
              confluence=False, sharepoint=False,
              sparx_ea=False,
              link_udpr=None):
    if model == TEST_MODEL:
        languages = 'en'
    optargs = []
    if languages is not None:
        optargs.append(f"--languages='{languages}'")
    if skip_odm:
        optargs.append("--skip-odm")
    if skip_web:
        optargs.append("--skip-web")
    if link_udpr is not None:
        optargs.append("--link-udpr=" + link_udpr)
    command = f"python dist/generator.py --model='{model}' {' '.join(optargs)}"
    print(f"Starting generator with: {command}")
    c.run(command)
