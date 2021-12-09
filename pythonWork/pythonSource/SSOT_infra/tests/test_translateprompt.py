from unittest import TestCase
import os
from pathlib import Path
import glob
import subprocess

from SSOT_infra import translateprompt
from SSOT_infra import resettransldomain, settransldomain, transl


# TODO Eventually move this into production code
def update_gettext_ressources(translation_root: str) -> int:
    """Update .mo cache from .po translation sources
    Will run `msgfmt -o FOLDER/de/LC_MESSAGES/confluence-publisher.mo FOLDER/de/LC_MESSAGES/confluence-publisher.po`
    @:return Number of updated ressources
    """
    sources = glob.glob(translation_root + '/**/*.po', recursive=True)
    for po_source in sources:
        pre, ext = os.path.splitext(po_source)
        mo_target = pre + '.mo'
        subprocess.check_output(['msgfmt', '-o', mo_target, po_source])
    print(f"Upated {len(sources)} files")


class TestDrawIoDiagramGeneration(TestCase):

    def setUp(self) -> None:
        """Initialize translation content"""
        assert os.path.exists(
            translateprompt.LOCALES_DIREC), f"Missing locales directory {translateprompt.LOCALES_DIREC}"
        update_gettext_ressources(translateprompt.LOCALES_DIREC)

    def test_transl(self):
        # default ist input
        resettransldomain()
        assert transl("") == ""
        assert transl("Entität") == "Entität"
        # englisch
        settransldomain("en")
        assert transl("Entität") == "Entity"
        # französisch
        settransldomain("fr")
        assert transl("Entität") == "Entité"
        # check specific language other than set language
        assert transl("Entität", "de") == "Entität"
        assert transl("Entität", "en") == "Entity"
        assert transl("Entität", "fr") == "Entité"
        # unbekannte Sprache defaults to en
        settransldomain("xi")
        assert transl("Entität") == "Entity"
        # de = deutsch
        settransldomain("de")
        assert transl("Entität") == "Entität"
        # and back to default
        resettransldomain()
        assert transl("Entität") == "Entität"
