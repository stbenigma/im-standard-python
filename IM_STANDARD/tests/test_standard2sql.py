import unittest
from pathlib import Path
import pytest

from IM_STANDARD.imstandard2sql import Standardmodel2SQLdatabase
from IM_STANDARD.SQL.SQL_STANDARD import StandardModelDb
from IM_STANDARD.SQL.SQL_INFRA import SqliteDb
from IM_STANDARD.JSON import jsonvalidation


class Test_standard2sql(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog, tmp_path, capsys):
        self.caplog = caplog
        self.capsys = capsys
        self.temppath = Path(tmp_path)

    def setUp(self) -> None:
        self.mydebugpath = (Path.home() / "Downloads") if (Path.home() / "Downloads").exists() else self.temppath
        return

    def test_simple(self):
        struct={
  "ModelInfo": {
    "elementId": "MODL1",
    "modelName": "IM-Standard",
    "modelType": "Information model",
    "mainLanguage": "de",
    "modelVersion": "0.0",
    "languages": [
      "de",
      "en"
    ],
    "targetEnvironment": "???",
    "additionalProps": {
      "uc": "ich",
      "dc": "2026-06-17T10:29:49.270408"
    }
  },
            "Categories": [
                {
                    "elementId": "CATG8",
                    "name": {
                        "de": "Beziehungen",
                        "en": "Relations"
                    },
                    "description": {
                        "de": "Gruppiere alle Entitäten zum Thema Beziehungen",
                        "en": "Group all entities of regarding relationships"
                    },
                    "categoryId": "CATG7",
                    "modelId": "MODL1",
                    "additionalProps": {
                        "FULLPATH": "Software Engineering Modell:Semantische, fachliche Modelle/Informationsmodelle/Kernmodell/Beziehungen",
                        "SOURCE-ID": "3aebd254-1119-4e07-9b97-1d3f4a6b3674",
                        "SOURCE-MODEL": "Software Engineering Modell",
                        "uc": "stb@foryouandyourcustomers.com",
                        "dc": "2025-07-14T17:46:22.207000"
                    },
                    "categoryType": "ENTITY"
                },
                {
                    "elementId": "CATG9",
                    "name": {
                        "de": "Entitäten",
                        "en": "Entities"
                    },
                    "description": {
                        "de": "Gruppierung der Elemente rund um die Entität",
                        "en": "Group all entities of regarding entities"
                    },
                    "categoryId": "CATG7",
                    "modelId": "MODL1",
                    "additionalProps": {
                        "FULLPATH": "Software Engineering Modell:Semantische, fachliche Modelle/Informationsmodelle/Kernmodell/Entitäten",
                        "SOURCE-ID": "0a76397f-1411-4061-b604-35f2db183f68",
                        "SOURCE-MODEL": "Software Engineering Modell",
                        "uc": "stb@foryouandyourcustomers.com",
                        "dc": "2025-07-14T17:50:39.389000"
                    },
                    "categoryType": "ENTITY"
                },
                {
                    "elementId": "CATG6",
                    "name": {
                        "de": "Erweitertes Modell",
                        "en": "Erweitertes Modell"
                    },
                    "description": {
                        "de": "The core model consists of the basic elements according to relational theory.\n\nTheoretically, an information model can only be formed completely with these elements.\n\nFor practical applications, however, it makes sense to introduce extended elements that offer simplifications for readability and administration. \nBut they can all be clearly mapped to concepts of the core model. In other words, they are additions that do not corrupt the strictness of the core model.",
                        "en": "The extended model consists of the elements to ease the usage of the basic model.\n\nThey can all be clearly mapped to concepts of the core model. In other words, they are additions that do not corrupt the strictness of the core model."
                    },
                    "categoryId": "CATG5",
                    "modelId": "MODL1",
                    "additionalProps": {
                        "FULLPATH": "Software Engineering Modell:Semantische, fachliche Modelle/Informationsmodelle/Erweitertes Modell",
                        "SOURCE-ID": "ed7652a3-d76b-44eb-afbf-98ac5a015ab5",
                        "SOURCE-MODEL": "Software Engineering Modell",
                        "order": "2",
                        "uc": "stb@foryouandyourcustomers.com",
                        "dc": "2025-07-14T10:19:45.913000"
                    },
                    "categoryType": "ENTITY"
                },
                {
                    "elementId": "CATG4",
                    "name": {
                        "de": "Generische Modellelemente",
                        "en": "Generische Modellelemente"
                    },
                    "description": {
                        "de": "Informationen, die für (fast) jedes Element des gesamten SE-Modells genutzt angegeben werden können.",
                        "en": "Informationen, die für (fast) jedes Element des gesamten SE-Modells genutzt angegeben werden können."
                    },
                    "categoryId": "CATG2",
                    "modelId": "MODL1",
                    "additionalProps": {
                        "FULLPATH": "Software Engineering Modell:Organisation Metamodell/Generische Modellelemente",
                        "SOURCE-ID": "76bb0c89-22d8-4487-9735-87fbcefb5272",
                        "SOURCE-MODEL": "Software Engineering Modell",
                        "uc": "stb@foryouandyourcustomers.com",
                        "dc": "2025-12-14T17:13:59.994000"
                    },
                    "categoryType": "ENTITY"
                },
                {
                    "elementId": "CATG5",
                    "name": {
                        "de": "Informationsmodelle",
                        "en": "Information models"
                    },
                    "description": {
                        "de": "Dieses Informationsmodell ist das Metamodell für Informationsmodelle.\nEs beschreibt was wir (alle die diesen Standard akzeptieren) unter einem Informationsmodell verstehen, wie es aufgebaut ist und wir es nutzen sollen.\n\nsiehe auch: www.informationsmodellierung.ch/",
                        "en": "This information model is the meta model for information models.\nIt describes what we (all those who accept this standard) understand by an information model, how it is structured and how we should use it.\n\nSee also: www.informationsmodellierung.ch/"
                    },
                    "categoryId": "CATG3",
                    "modelId": "MODL1",
                    "additionalProps": {
                        "FULLPATH": "Software Engineering Modell:Semantische, fachliche Modelle/Informationsmodelle",
                        "SOURCE-ID": "6e8e189a-54bc-4722-af4d-9a0305632bd0",
                        "SOURCE-MODEL": "Software Engineering Modell",
                        "order": "1",
                        "uc": "stb@foryouandyourcustomers.com",
                        "dc": "2025-12-01T08:55:46.117000"
                    },
                    "categoryType": "ENTITY"
                },
                {
                    "elementId": "CATG7",
                    "name": {
                        "de": "Kernmodell",
                        "en": "Base model"
                    },
                    "description": {
                        "de": "Das Kernmodell sind die grundlegenden Elemente gemäss der relationalen Theorie.\n\nTheoretisch kann ein Informaionsmodell vollständig nur mit diesen Elementen gebildet werden.\nFür praktische Anwendungen macht es aber Sinn erweiterte Elemente einzuführen, die Vereinfachungen für die Lesbarkeit und Verwaltung anbieten. \nAber sie sind alle eindeutig auf Konzepte des Kernmodells abbildbar. D.h. es sind Zusätze, die die Striktheit des Kernmodells nicht korrumpieren.",
                        "en": "The core model consists of the basic elements according to relational theory.\n\nTheoretically, an information model can only be formed completely with these elements.\n\nFor practical applications, however, it makes sense to introduce extended elements that offer simplifications for readability and administration. \nBut they can all be clearly mapped to concepts of the core model. In other words, they are additions that do not corrupt the strictness of the core model."
                    },
                    "categoryId": "CATG5",
                    "modelId": "MODL1",
                    "additionalProps": {
                        "FULLPATH": "Software Engineering Modell:Semantische, fachliche Modelle/Informationsmodelle/Kernmodell",
                        "SOURCE-ID": "328b4425-3a07-488a-9b9e-1390b98b3d72",
                        "SOURCE-MODEL": "Software Engineering Modell",
                        "order": "1",
                        "uc": "stb@foryouandyourcustomers.com",
                        "dc": "2025-07-14T10:19:45.913000"
                    },
                    "categoryType": "ENTITY"
                },
                {
                    "elementId": "CATG2",
                    "name": {
                        "de": "Organisation Metamodell",
                        "en": "Orgnisational meta model"
                    },
                    "description": {
                        "de": "Im Metamodell sind Informationen die der Begründung, Verwaltung und Referenzierung von Modellelemente dienen. Beispiele Referenzdokumente, Verantwortlichkeiten, Sicherheitsanforderungen.",
                        "en": "Im Metamodell sind Informationen die der Begründung, Verwaltung und Referenzierung von Modellelemente dienen. Beispiele Referenzdokumente, Verantwortlichkeiten, Sicherheitsanforderungen."
                    },
                    "modelId": "MODL1",
                    "additionalProps": {
                        "FULLPATH": "Software Engineering Modell:/Organisation Metamodell",
                        "SOURCE-ID": "814c4d09-2ed6-4a85-b9d7-35fb0d112470",
                        "SOURCE-MODEL": "Software Engineering Modell",
                        "order": "9",
                        "uc": "stb@foryouandyourcustomers.com",
                        "dc": "2025-11-27T20:44:42.937000"
                    },
                    "categoryType": "ENTITY"
                },
                {
                    "elementId": "CATG3",
                    "name": {
                        "de": "Semantische, fachliche Modelle",
                        "en": "Semantic, business related models"
                    },
                    "description": {
                        "de": "Semantische Modelle, die ausschliesslich Begriffe, Bedeutungen, Zusammenhänge und Intentionen für Menschen klären. Es dient der unmissverständlichen Kommunikation zwichen Menschen im Bereich in dem diese Modell gültig sind.\n\nEs umfasst Informationen wie Fachwissen, Informationsmodelle, Geschäftsprozess Modelle, Business-Glossare, Ontologien, Referenzen.\n\nSemantische Modelle sind technologie‑agnostisch, verwenden Fachsprache und dienen als gemeinsame Sicht für Fachbereich, Architekten und Entwickler; sie reduzieren Semantik‑Streit in allen Phasen der Softwareentwicklung.",
                        "en": "Semantic models that exclusively clarify terms, meanings, contexts and intentions for humans. They serve to enable unambiguous communication between humans in the area in which these models are valid.\n\nThey comprise information such as specialist knowledge, information models, business process models, business glossaries, ontologies and references.\n\nSemantic models are technology-agnostic, use technical language and serve as a common view for subject matter experts, architects and developers; they reduce semantic disputes in all phases of software development."
                    },
                    "modelId": "MODL1",
                    "additionalProps": {
                        "Delimitation": "Semantische Modelle machen **keine** Angaben zu technischer Darsstellung, Umsetzung, Speicherung, Verarbeitung von Daten.",
                        "FULLPATH": "Software Engineering Modell:/Semantische, fachliche Modelle",
                        "SOURCE-ID": "111cbc16-a3e2-45dd-a3d9-7190a01b09a7",
                        "SOURCE-MODEL": "Software Engineering Modell",
                        "uc": "stb@foryouandyourcustomers.com",
                        "dc": "2025-12-14T15:48:27.254000"
                    },
                    "categoryType": "ENTITY"
                },
                {
                    "elementId": "CATG10",
                    "name": {
                        "de": "Wertebereiche",
                        "en": "Domains"
                    },
                    "description": {
                        "de": "Gruppiere alle Entitäten zum Thema Wertebereiche",
                        "en": "Group all entities regarding domains"
                    },
                    "categoryId": "CATG7",
                    "modelId": "MODL1",
                    "additionalProps": {
                        "FULLPATH": "Software Engineering Modell:Semantische, fachliche Modelle/Informationsmodelle/Kernmodell/Wertebereiche",
                        "SOURCE-ID": "f65a3570-1e40-4ef7-bc56-d4019c0c880a",
                        "SOURCE-MODEL": "Software Engineering Modell",
                        "uc": "stb@foryouandyourcustomers.com",
                        "dc": "2025-07-14T10:54:36.910000"
                    },
                    "categoryType": "ENTITY"
                }
            ],
        }
        mydb=StandardModelDb(sqlitedb=SqliteDb())
        db=Standardmodel2SQLdatabase(jsonmodel=struct,
                                     mydb=mydb).filldatabase()
        mydb.writedbtofile(filepath=self.mydebugpath / "json2sql.db")
        return

    def test_IM(self):
        testfile=Path(__file__).parent.parent / "tests" / "json-test-standard-files" / "Informationsmodell-modell-standard.json"
        if not testfile.is_file():
            self.skipTest(f"testfile not found: {testfile}")
        struct= jsonvalidation.ValidateJsonModel.readjsonfromfile(filepath=testfile)
        mydb=StandardModelDb(sqlitedb=SqliteDb())
        db=Standardmodel2SQLdatabase(jsonmodel=struct,
                                     mydb=mydb).filldatabase()
        mydb.writedbtofile(filepath=self.mydebugpath / "json2sql.db")
        return


if __name__ == '__main__':
    unittest.main()
