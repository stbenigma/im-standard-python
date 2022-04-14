from unittest import TestCase
import os
import glob
import subprocess

from SSOT_infra import translateprompt
from SSOT_infra import resettransldomain, settransldomain, transl


# TODO Eventually move this into production code
def update_gettext_ressources(translation_root: str
                              = translateprompt.LOCALES_DIREC) -> int:
    """Update .mo cache from .po translation sources
    Will run `msgfmt -o FOLDER/de/LC_MESSAGES/confluence-publisher.mo FOLDER/de/LC_MESSAGES/confluence-publisher.po`
    @:return Number of updated ressources
    """
    assert os.path.exists(translation_root), \
        f"Missing locales directory {translation_root}"

    sources = glob.glob(translation_root + '/**/*.po', recursive=True)
    for po_source in sources:
        pre, ext = os.path.splitext(po_source)
        mo_target = pre + '.mo'
        subprocess.check_output(['msgfmt', '-o', mo_target, po_source])
    print(f"Upated {len(sources)} files")
    return len(sources)


class TestTranslation(TestCase):

    def setUp(self) -> None:
        update_gettext_ressources(translateprompt.LOCALES_DIREC)

    def test_transl(self):
        # default ist input
        resettransldomain()
        assert transl("") == ""
        assert transl("Entität") == "Entität"
        # englisch
        settransldomain("en")
        assert transl("Entität") == "Entity"
        assert transl("Attribut") == "Attribute"
        assert transl("entität") == "entität"  # do not translate if lowercase
        # französisch
        settransldomain("fr")
        assert transl("Entität") == "Entité"
        assert transl("Attribut") == "Attribut"
        # check specific language other than set language
        assert transl("Entität", "de") == "Entität"
        assert transl("Entität", "en") == "Entity"
        assert transl("Entität", "fr") == "Entité"
        assert transl("YEAR", "de") == "Jahr"
        assert transl("Year", "de") != "Jahr"
        assert transl("YEAR", "en") == "Year"
        assert transl("YEAR", "fr") == "Anneé"

        # unbekannte Sprache defaults to en
        settransldomain("xi")
        assert transl("Entität") == "Entität"
        # de = deutsch
        settransldomain("de")
        assert transl("Entität") == "Entität"
        # and back to default
        resettransldomain()
        assert transl("Entität") == "Entität"
