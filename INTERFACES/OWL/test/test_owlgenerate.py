import unittest

from INTERFACES.OWL import generate_owl_turtle_from_im

class MyTestCase(unittest.TestCase):
    def test_example(self):
        ttl=generate_owl_turtle_from_im(im_data =
        {
  "ModelInfo": {
    "modelName": "Beispielmodell Astronomie",
    "modelType": "Information model",
    "mainLanguage": "de",
    "modelVersion": "0.9",
    "languages": [
      "de",
      "en"
    ],
    "targetEnvironment": "Informatiosmodell Standard",
    "originTool": "dataspot"
  },
  "Categories": [
    {
      "elementId": "CATG10",
      "name": {
        "de": "Astronomie Wertebereiche"
      },
      "categoryType": "DOMAIN"
    },
    {
      "elementId": "CATG11",
      "name": {
        "de": "Astronomie Referenzdaten"
      },
      "categoryType": "DOMAIN"
    },
    {
      "elementId": "CATG1",
      "name": {
        "de": "Astronomische Wertebereiche"
      },
      "categoryType": "DOMAIN",
      "parent": "CATG10"
    },
    {
      "elementId": "CATG2",
      "name": {
        "de": "Standard Datatypen",
        "en": "Standard data domains"
      },
      "categoryType": "DOMAIN",
      "parent": "CATG10"
    },
    {
      "elementId": "CATG3",
      "name": {
        "de": "Basis Wertebereiche",
        "en": "Base data domains"
      },
      "categoryType": "DOMAIN",
      "parent": "CATG2"
    },
    {
      "elementId": "CATG4",
      "name": {
        "de": "Physikalische Datentypen",
        "en": "Physical datatypes"
      },
      "categoryType": "DOMAIN",
      "parent": "CATG2"
    },
    {
      "elementId": "CATG10",
      "name": {
        "de": "Astronomie Wertebereiche"
      },
      "categoryType": "DOMAIN"
    },
    {
      "elementId": "CATG5",
      "name": {
        "de": "Astronomische Referenzwerte",
        "en": "Astronomical reference values"
      },
      "categoryType": "DOMAIN",
      "parent": "CATG11"
    },
    {
      "elementId": "CATG6",
      "name": {
        "de": "Standard Referenzwerte"
      },
      "categoryType": "DOMAIN",
      "parent": "CATG11"
    },
    {
      "elementId": "CATG11",
      "name": {
        "de": "Astronomie Referenzdaten"
      },
      "categoryType": "DOMAIN"
    },
    {
      "elementId": "CATG7",
      "name": {
        "de": "Sternsystem",
        "en": "Star system"
      },
      "categoryType": "ENTITY"
    },
    {
      "elementId": "CATG8",
      "name": {
        "de": "Grosse Objekte",
        "en": "Large objects"
      },
      "categoryType": "ENTITY",
      "parent": "CATG7"
    },
    {
      "elementId": "CATG9",
      "name": {
        "de": "Kleine Objekte",
        "en": "Small objects"
      },
      "categoryType": "ENTITY",
      "parent": "CATG7"
    }
  ],
  "Domains": [
    {
      "elementId": "DOMA26",
      "name": {
        "de": "Leuchtklasse",
        "en": "Luminosity class"
      },
      "description": {
        "de": "Leuchtkraftklassen (Helligkeitstypen) \nI\t\u00dcberriesen\tBetelgeuse (M1I)\nII\tHelle Riesen\t\nIII\tRiesen\tAldebaran (K5III)\nIV\tUnterriesen\t\nV\tHauptreihe (normale Sterne)\tSonne (G2V)\nVI\tUnterzwerge\t\nD\tWei\u00dfe Zwerge\tSirius B",
        "en": "Luminosity classes (brightness types)\nI Supergiant Betelgeuse (M1I)\nII Bright giants\nIII Giants Aldebaran (K5III)\nIV Subgiants\nV Main sequence (normal stars) Sun (G2V)\nVI Subdwarfs\nD White dwarfs Sirius B"
      },
      "categoryId": "CATG5",
      "domainType": "LOVDomain",
      "values": [
        {
          "value": "VI",
          "displayValue": {
            "de": "Unterzwerge",
            "en": "Subdwarfs"
          },
          "description": {
            "de": "auch sd, Betelgeuse (M1I)"
          }
        },
        {
          "value": "III",
          "displayValue": {
            "de": "Riesen",
            "en": "Giants"
          },
          "description": {
            "de": "Aldebaran (K5III)"
          }
        },
        {
          "value": "I",
          "displayValue": {
            "de": "\u00dcberriese",
            "en": "Supergiant"
          },
          "description": {
            "de": "Unterteilung der \u00dcberriesen nach abnehmender Leuchtkraft Ia-0, Ia, Iab, Ib"
          }
        },
        {
          "value": "V",
          "displayValue": {
            "de": "Hauptreihe",
            "en": "Main sequence"
          },
          "description": {
            "de": "normale Stern, Sonne (G2V)"
          }
        },
        {
          "value": "0",
          "displayValue": {
            "de": "Hyperriese",
            "en": "Supergiant"
          },
          "description": {
            "de": "Deneb, S Doradus"
          }
        },
        {
          "value": "VII",
          "displayValue": {
            "de": "Wei\u00dfe Zwerge",
            "en": "White dwarf"
          },
          "description": {
            "de": "Auch D,  Sirius B"
          }
        },
        {
          "value": "IV",
          "displayValue": {
            "de": "Unterriesen",
            "en": "Subgiants"
          }
        },
        {
          "value": "II",
          "displayValue": {
            "de": "Helle Riesen",
            "en": "Bright Giants"
          }
        }
      ]
    },
    {
      "elementId": "DOMA27",
      "name": {
        "de": "Oberfl\u00e4chenbeschaffenheit",
        "en": "Surface composition"
      },
      "description": {
        "de": "Beschaffenheit der Oberl\u00e4che eines Planeten.\nFest, Gas, Eis",
        "en": "Nature of the surface of a planet.\nSolid, gas, ice"
      },
      "categoryId": "CATG5",
      "domainType": "LOVDomain",
      "values": [
        {
          "value": "Eis",
          "description": {
            "de": "Wasser, Ammoniak und Methan in Form von Eis, keine feste Oberfl\u00e4che."
          }
        },
        {
          "value": "Gestein",
          "description": {
            "de": "Gestein und Metallen, feste Oberfl\u00e4che."
          }
        },
        {
          "value": "Gas",
          "description": {
            "de": "Wasserstoff und Helium, keine feste Oberfl\u00e4che."
          }
        }
      ]
    },
    {
      "elementId": "DOMA28",
      "name": {
        "de": "Unterleuchtklasse"
      },
      "description": {
        "de": "Unterteilung der \u00dcberriesen nach abnehmender Leuchtkraft"
      },
      "categoryId": "CATG5",
      "domainType": "LOVDomain",
      "values": [
        {
          "value": "ab",
          "displayValue": {
            "de": "dritthellste"
          }
        },
        {
          "value": "b",
          "displayValue": {
            "de": "dunklste"
          }
        },
        {
          "value": "a",
          "displayValue": {
            "de": "zweithellste"
          }
        },
        {
          "value": "a-0",
          "displayValue": {
            "de": "hellste"
          }
        }
      ]
    },
    {
      "elementId": "DOMA29",
      "name": {
        "de": "Zeitangabe",
        "en": "Time indication"
      },
      "description": {
        "de": "Liste der Zeitangaben f\u00fcr Umlaufdauern \nStunde, Tag, Jahr"
      },
      "categoryId": "CATG5",
      "domainType": "LOVDomain",
      "values": [
        {
          "value": "tag",
          "displayValue": {
            "de": "Tag"
          }
        },
        {
          "value": "std",
          "displayValue": {
            "de": "Stunde"
          }
        },
        {
          "value": "jahr",
          "displayValue": {
            "de": "Jahr"
          }
        }
      ]
    },
    {
      "elementId": "DOMA30",
      "name": {
        "de": "Kalender Einheiten",
        "en": "Physical unit"
      },
      "description": {
        "en": "Standardised (SI) physical units"
      },
      "categoryId": "CATG6",
      "domainType": "LOVDomain",
      "values": [
        {
          "value": "year",
          "displayValue": {
            "de": "Jahr"
          },
          "description": {
            "de": "Kalenderjahr (365, 366 Tage)"
          }
        },
        {
          "value": "sem",
          "displayValue": {
            "de": "Semester"
          },
          "description": {
            "de": "2 Quartale, 6 Monate"
          }
        },
        {
          "value": "min",
          "displayValue": {
            "de": "Minute"
          },
          "description": {
            "de": "60 Sekunden"
          }
        },
        {
          "value": "week",
          "displayValue": {
            "de": "Woche"
          },
          "description": {
            "de": "7 Tage"
          }
        },
        {
          "value": "s",
          "displayValue": {
            "de": "Sekunde",
            "en": "second"
          },
          "description": {
            "de": "Grundeinheit",
            "en": "Duration of time"
          }
        },
        {
          "value": "day",
          "displayValue": {
            "de": "Tag"
          },
          "description": {
            "de": "24 Stunden"
          }
        },
        {
          "value": "mon",
          "displayValue": {
            "de": "Monat"
          },
          "description": {
            "de": "Kalendermonat mit 28-31 Tagen"
          }
        },
        {
          "value": "hour",
          "displayValue": {
            "de": "Stunde"
          },
          "description": {
            "de": "60 Minuten"
          }
        },
        {
          "value": "q",
          "displayValue": {
            "de": "Quartal"
          },
          "description": {
            "de": "3 Monate"
          }
        },
        {
          "value": "ns",
          "displayValue": {
            "de": "Nanosekunde",
            "en": "nanosecond"
          },
          "description": {
            "de": "10^-9 s",
            "en": "10^-9 s"
          }
        },
        {
          "value": "ms",
          "displayValue": {
            "de": "Millisekunde",
            "en": "millisecond"
          },
          "description": {
            "de": "1/1000 s",
            "en": "1/1000 s"
          }
        }
      ]
    },
    {
      "elementId": "DOMA31",
      "name": {
        "de": "Physikalische Einheit",
        "en": "Physical unit"
      },
      "description": {
        "en": "Standardised (SI) physical units"
      },
      "categoryId": "CATG6",
      "domainType": "LOVDomain",
      "values": [
        {
          "value": "mol",
          "displayValue": {
            "de": "Mol",
            "en": "mol"
          },
          "description": {
            "de": "Stoffmenge",
            "en": "Amount of substance"
          }
        },
        {
          "value": "K",
          "displayValue": {
            "de": "Kelvin",
            "en": "kelvin"
          },
          "description": {
            "de": "Temperatur",
            "en": "Temperature"
          }
        },
        {
          "value": "kg",
          "displayValue": {
            "de": "Kilogramm",
            "en": "kilogram"
          },
          "description": {
            "de": "Masse",
            "en": "Mass"
          }
        },
        {
          "value": "A",
          "displayValue": {
            "de": "Ampere",
            "en": "ampere"
          },
          "description": {
            "de": "Elektrische Stromst\u00e4rke",
            "en": "Electric current"
          }
        },
        {
          "value": "t",
          "displayValue": {
            "de": "Tonne",
            "en": "ton"
          },
          "description": {
            "de": "1000 kg",
            "en": "1000 kg"
          }
        },
        {
          "value": "s",
          "displayValue": {
            "de": "Sekunde",
            "en": "second"
          },
          "description": {
            "de": "Zeitdauer",
            "en": "Duration of time"
          }
        },
        {
          "value": "cd",
          "displayValue": {
            "de": "Candela",
            "en": "candela"
          },
          "description": {
            "de": "Lichtst\u00e4rke",
            "en": "Luminous intensity"
          }
        },
        {
          "value": "m",
          "displayValue": {
            "de": "Meter",
            "en": "meter"
          },
          "description": {
            "de": "L\u00e4nge, Distanz",
            "en": "Length, distance"
          }
        }
      ]
    },
    {
      "elementId": "DOMA1",
      "name": {
        "de": "Galaktische Entfernung",
        "en": "Galactical distance"
      },
      "description": {
        "de": "Abstand zwischen 2 Objekten im galaktischen Umfeld\n \nEinheit sind Lichtjahre. Ein LJ entspricht 63241 AE oder \u2248 9.46 Billionen km",
        "en": "Distance between 2 objects in the galactic neighbourhood\n \nThe unit is light years. One LJ corresponds to 63241 AU or \u2248 9.46 trillion kilometres"
      },
      "categoryId": "CATG1",
      "domainType": "NumericDomain",
      "minValue": 0,
      "maxValue": 150000,
      "totalDigits": 9,
      "fractDigits": 3,
      "unit": "LJ"
    },
    {
      "elementId": "DOMA2",
      "name": {
        "de": "Himmelsk\u00f6rper Durchmesser",
        "en": "Celestial body diameter"
      },
      "categoryId": "CATG1",
      "domainType": "GroupDomain",
      "elements": [
        {
          "elementId": "ATTR3",
          "name": {
            "de": "\u00c4quatordurchmesser",
            "en": "Equator diameter"
          },
          "mandatory": False,
          "displaySeq": 3,
          "description": {
            "de": "Typischerweise der l\u00e4ngste Durchmesser.\nWegen der Rotation sind kugelf\u00f6rmige Himmelsk\u00f6per am \u00c4quator *ausgebeult*",
            "en": "Typically the longest diameter.\nDue to rotation, spherical celestial bodies are *dent out* at the equator"
          },
          "shortDescr": {
            "de": "Durchmesser 90\u00ba zur Rotationsaches",
            "en": "Diameter 90\u00ba to the axis of rotation"
          },
          "repeated": False
        },
        {
          "elementId": "ATTR4",
          "name": {
            "de": "Mittlerer Durchmesser",
            "en": "Average diameter"
          },
          "mandatory": True,
          "displaySeq": 1,
          "description": {
            "de": "Der Durchmesser, den man bei nicht sehr genauen angaben oder einfachen astronomischen / pyhsikalischen Berechnungen verwendet",
            "en": "The diameter used for not very precise specifications or simple astronomical / physical calculations"
          },
          "shortDescr": {
            "de": "Mittlerer Durchmesser einer idealen Kugel",
            "en": "Average diameter of an ideal sphere"
          },
          "repeated": False
        },
        {
          "elementId": "ATTR5",
          "name": {
            "de": "Poldurchmesser",
            "en": "Pole diameter"
          },
          "mandatory": False,
          "displaySeq": 2,
          "description": {
            "de": "Typischerweise der kleinste Durchmesser.\nWegen der Rotation sind kugelf\u00f6rmige Himmelsk\u00f6per am \u00c4quator *ausgebeult*",
            "en": "Typically the smallest diameter.\nDue to rotation, spherical celestial bodies are *dent out* at the equator"
          },
          "shortDescr": {
            "de": "Durchmesser entlang der Rotationsachse",
            "en": "Diameter along the axis of rotation"
          },
          "repeated": False
        }
      ]
    },
    {
      "elementId": "DOMA3",
      "name": {
        "de": "Jahrzahl",
        "en": "Year"
      },
      "description": {
        "de": "Bei Berechnungen mit Jahrzahlen (Anzahl Jahre zwischen 2 Jahrzahlen) ist zu ber\u00fccksichtigen, dass es die Jahrzahl 0 nicht gibt",
        "en": "When calculating with year numbers (number of years between 2 year numbers), it must be taken into account that the year 0 does not exist"
      },
      "categoryId": "CATG1",
      "domainType": "NumericDomain",
      "minValue": -5000,
      "maxValue": 5000,
      "totalDigits": 4
    },
    {
      "elementId": "DOMA4",
      "name": {
        "de": "Sternsystem Entfernung",
        "en": "Startsystem distance"
      },
      "description": {
        "de": "Abstand zwischen 2 Punkten oder Objekten innerhalb eines Sternensystems\n\nDie Einheit ist 1000km. \n\nDie Abst\u00e4nde sind in der Gr\u00f6ssenordnung des Durchmessers eines Sternensystems. D.h. bis ca 200 Astronomsiche Einheiten (AE) (=30*10^9km)\n\nEine AE entspricht ca 150Mio Km (genau 149.597.870,7) (entspricht 8,317\u00a0Lichtminuten",
        "en": "Distance between 2 points or objects within a star system\n\nThe unit is 1000km.\n\nThe distances are in the order of magnitude of the diameter of a star system. I.e. up to approx. 200 astronomical units (AU) (=30*10^9km)\n\nOne AU corresponds to approx. 150 million kilometres (exactly 149,597,870.7) (corresponds to 8.317 light minutes\")."
      },
      "categoryId": "CATG1",
      "domainType": "NumericDomain",
      "minValue": 0,
      "maxValue": 10000000,
      "unit": "10^3 km"
    },
    {
      "elementId": "DOMA5",
      "name": {
        "de": "Umlaufdauer",
        "en": "Cycle time"
      },
      "description": {
        "de": "Dauer die ein Begleiter braucht um sein Mutterobjekt zu umkreisen.\nGruppenattribut mit Wert und Einheit (Stunde, Tag, Jahr).",
        "en": "Duration that a companion needs to orbit its parent object.\nGroup attribute with value and unit (hour, day, year)."
      },
      "categoryId": "CATG1",
      "domainType": "GroupDomain",
      "elements": [
        {
          "elementId": "ATTR8",
          "name": {
            "de": "Dauer",
            "en": "Duration"
          },
          "mandatory": True,
          "domainId": "DOMA8",
          "displaySeq": 1,
          "description": {
            "de": "Anzahl der Einheiten, die im Schwesterfeld definiert ist",
            "en": "Number of units defined in the sister field"
          },
          "shortDescr": {
            "de": "Anzahl Zeiteinheiten",
            "en": "Number of time units"
          },
          "repeated": False,
          "minValue": 1.0
        },
        {
          "elementId": "ATTR9",
          "name": {
            "de": "Einheit"
          },
          "mandatory": True,
          "domainId": "DOMA29",
          "displaySeq": 2,
          "description": {
            "de": "Zeiteinheit als Stunde, Tag oder Jahr"
          },
          "shortDescr": {
            "de": "Zeiteinheit"
          },
          "repeated": False
        }
      ]
    },
    {
      "elementId": "DOMA6",
      "name": {
        "de": "Booelan",
        "en": "Boolean"
      },
      "categoryId": "CATG3",
      "domainType": "BooleanDomain"
    },
    {
      "elementId": "DOMA7",
      "name": {
        "de": "Datum",
        "en": "Date"
      },
      "description": {
        "de": "Negative Daten (vor unserer Zeit) werden mit VUZ markiert",
        "en": "Negative dates (before our time) are marked with VUZ"
      },
      "categoryId": "CATG3",
      "domainType": "DatetimeDomain",
      "granularity": "DAY"
    },
    {
      "elementId": "DOMA8",
      "name": {
        "de": "Dezimalzahl",
        "en": "Decimal"
      },
      "categoryId": "CATG3",
      "domainType": "NumericDomain"
    },
    {
      "elementId": "DOMA9",
      "name": {
        "de": "Integer",
        "en": "Ganzzahl"
      },
      "categoryId": "CATG3",
      "domainType": "NumericDomain"
    },
    {
      "elementId": "DOMA10",
      "name": {
        "de": "String",
        "en": "String"
      },
      "categoryId": "CATG3",
      "domainType": "TextDomain"
    },
    {
      "elementId": "DOMA11",
      "name": {
        "de": "Text",
        "en": "Text"
      },
      "categoryId": "CATG3",
      "domainType": "TextDomain"
    },
    {
      "elementId": "DOMA12",
      "name": {
        "de": "Uhrzeit",
        "en": "Time of day"
      },
      "description": {
        "de": "Zeit innerhalb des Tages\n00:00:00 - 23:59:59",
        "en": "Time within the day\n00:00:00 - 23:59:59"
      },
      "categoryId": "CATG3",
      "domainType": "TextDomain",
      "syntaxRule": "^[0-1][0-9]:[0-5][0-9]$"
    },
    {
      "elementId": "DOMA13",
      "name": {
        "de": "Zeitstempel",
        "en": "Timestamp"
      },
      "description": {
        "de": "Punkt auf der Zeitachse auf die Milisekunde genau",
        "en": "Point on the time axis accurate to the millisecond"
      },
      "categoryId": "CATG3",
      "domainType": "DatetimeDomain",
      "granularity": "MINUTE"
    },
    {
      "elementId": "DOMA14",
      "name": {
        "de": "Distanz [km]",
        "en": "Distance [km]"
      },
      "categoryId": "CATG4",
      "domainType": "NumericDomain",
      "minValue": 0,
      "totalDigits": 13,
      "fractDigits": 3,
      "unit": "km"
    },
    {
      "elementId": "DOMA15",
      "name": {
        "de": "Distanz [m]",
        "en": "Distance [m]"
      },
      "categoryId": "CATG4",
      "domainType": "NumericDomain",
      "minValue": 0,
      "totalDigits": 9,
      "fractDigits": 3,
      "unit": "m"
    },
    {
      "elementId": "DOMA16",
      "name": {
        "de": "Distanz [mm]",
        "en": "Distance [m]"
      },
      "categoryId": "CATG4",
      "domainType": "NumericDomain",
      "minValue": 0,
      "totalDigits": 9,
      "fractDigits": 3,
      "unit": "mm"
    },
    {
      "elementId": "DOMA17",
      "name": {
        "de": "Distanz [nm]",
        "en": "Distance [nm]"
      },
      "description": {
        "de": "1 Nanometer = 10^-9 Meter",
        "en": "1 Nanometer = 10^-9 meter"
      },
      "categoryId": "CATG4",
      "domainType": "NumericDomain",
      "minValue": 0,
      "totalDigits": 9,
      "fractDigits": 3,
      "unit": "nm"
    },
    {
      "elementId": "DOMA18",
      "name": {
        "de": "Einheitsmenge",
        "en": "Unit quantity"
      },
      "description": {
        "de": "Menge von Einheiten als Gruppenattribut mit Menge und (physikalischer) Einheit, in der diese Menge gemessen wurde.",
        "en": "Group attribute: Quantity together with the (physical) unit in which this quantity was measured."
      },
      "categoryId": "CATG4",
      "domainType": "GroupDomain",
      "elements": [
        {
          "elementId": "ATTR1",
          "name": {
            "de": "Einheit",
            "en": "Unit"
          },
          "mandatory": True,
          "domainId": "DOMA31",
          "displaySeq": 2,
          "shortDescr": {
            "de": "Physikalische Einheit",
            "en": "physical unit"
          },
          "repeated": False
        },
        {
          "elementId": "ATTR2",
          "name": {
            "de": "Menge",
            "en": "Quantity"
          },
          "mandatory": True,
          "domainId": "DOMA20",
          "displaySeq": 1,
          "shortDescr": {
            "de": "Anzahl der Einheiten",
            "en": "Number of units"
          },
          "repeated": False
        }
      ]
    },
    {
      "elementId": "DOMA19",
      "name": {
        "de": "Masse",
        "en": "Mass"
      },
      "categoryId": "CATG4",
      "domainType": "NumericDomain",
      "minValue": 0,
      "unit": "kg"
    },
    {
      "elementId": "DOMA20",
      "name": {
        "de": "Menge",
        "en": "Quantity"
      },
      "description": {
        "de": "decimal"
      },
      "categoryId": "CATG4",
      "domainType": "NumericDomain"
    },
    {
      "elementId": "DOMA21",
      "name": {
        "de": "Messwert",
        "en": "Measured value"
      },
      "description": {
        "de": "Gemessene oder erhobene Werte werden h\u00e4ufig mit einem Vertrauensintervall angegeben, das die maximale Abweichung nach oben oder unten in % angibt.",
        "en": "Measured or collected values are often specified with a confidence interval, which indicates the maximum deviation upwards or downwards in %."
      },
      "categoryId": "CATG4",
      "domainType": "GroupDomain",
      "elements": [
        {
          "elementId": "ATTR6",
          "name": {
            "de": "Vertrauensintervall",
            "en": "Confidence interval"
          },
          "mandatory": False,
          "domainId": "DOMA24",
          "displaySeq": 5,
          "description": {
            "de": "Bereich (als Prozent des Messwertes) um den der gemessene Wert nach oben oder unten abweichen kann.",
            "en": "Range (as a percentage of the measured value) by which the measured value can deviate upwards or downwards."
          },
          "shortDescr": {
            "de": "vermutete relative/r Abweichung / Fehlerbereich",
            "en": "Presumed relative deviation / error range"
          },
          "repeated": False,
          "minValue": 0.0
        },
        {
          "elementId": "ATTR7",
          "name": {
            "de": "Wert",
            "en": "Value"
          },
          "mandatory": True,
          "domainId": "DOMA18",
          "displaySeq": 1,
          "shortDescr": {
            "de": "der gemessene Wert (mit Einheit)",
            "en": "measured value (with unit)"
          },
          "repeated": False
        }
      ]
    },
    {
      "elementId": "DOMA22",
      "name": {
        "de": "ISO Zeitpunkt",
        "en": "ISO Datetime"
      },
      "description": {
        "de": "Die Universal Coordinate Time ist die Zeit am Nullmeridian in der N\u00e4he von Greenwich, England. UTC ist ein Datumswert, der die ISO 8601-Grundform yyyymmddThhmmss+|-hhmm oder die erweiterte ISO 8601-Form yyyy-mm-ddThh:mm:ss+|-hh:mm verwendet.",
        "en": "Universal Coordinate Time is the time at the zero meridian, near Greenwich, England. UTC is a datetime value that uses the ISO 8601 basic form yyyymmddThhmmss+|\u2013hhmm or the ISO 8601 extended form yyyy-mm-ddThh:mm:ss+|\u2013hh:mm."
      },
      "categoryId": "CATG2",
      "domainType": "DatetimeDomain",
      "granularity": "MINUTE"
    },
    {
      "elementId": "DOMA23",
      "name": {
        "de": "Name",
        "en": "Name"
      },
      "description": {
        "de": "Nichtleere Zeichenfolge, benutzt um etwas zu benennen",
        "en": "Nonempty sequence of arbitrary chaeracters, used to name a thing."
      },
      "categoryId": "CATG2",
      "domainType": "TextDomain"
    },
    {
      "elementId": "DOMA24",
      "name": {
        "de": "Prozent (dezimal)",
        "en": "Percentage (decimal)"
      },
      "description": {
        "de": "Prozentzahl,gerundet auf 3 Nachkommastellen",
        "en": "Percentage, rounded to 3 fractional digits"
      },
      "categoryId": "CATG2",
      "domainType": "NumericDomain",
      "totalDigits": 7,
      "fractDigits": 3,
      "unit": "%"
    },
    {
      "elementId": "DOMA25",
      "name": {
        "de": "Prozent (integer)",
        "en": "Percentage (integer)"
      },
      "description": {
        "de": "Prozentzahl, auf ganze Zahl gerundet.",
        "en": "Percentage, rounded to a whole number."
      },
      "categoryId": "CATG2",
      "domainType": "NumericDomain",
      "totalDigits": 4,
      "unit": "%"
    }
  ],
  "Entities": [
    {
      "elementId": "ENTI1",
      "name": {
        "de": "Mond",
        "en": "Planets Moon"
      },
      "shortDescr": {
        "de": "Fester Himmelsk\u00f6rper der um einen Planeten kreist",
        "en": "Fixed celestial body orbiting a planet"
      },
      "examples": [
        "(Erd-)Mond",
        "Phobos",
        "Deimos",
        "Io",
        "Europa",
        "Ganymed",
        "Triton",
        "Charon"
      ],
      "attributes": [],
      "keys": [
        [
          "RELA2",
          "RELA7"
        ]
      ]
    },
    {
      "elementId": "ENTI2",
      "name": {
        "de": "Planet"
      },
      "shortDescr": {
        "de": "Fester oder gasf\u00f6rmiger Himmelsk\u00f6rper der um einen Stern kreist",
        "en": "Solid or gaseous celestial body orbiting a star"
      },
      "examples": [
        "Jupiter",
        "Mars",
        "Neptun",
        "LHS 1140 b",
        "Proxima Centauri b",
        "Kepler-186f"
      ],
      "attributes": [
        {
          "elementId": "ATTR17",
          "name": "Oberfl\u00e4chentyp",
          "mandatory": False,
          "domainId": "DOMA27",
          "description": "Material, das die \u00e4usserste Schicht des Himmelsk\u00f6pers bildet.",
          "shortDescr": "Zustandsform der Oberfl\u00e4che",
          "examples": [
            "Feststoff",
            "Gas",
            "Eis"
          ]
        }
      ],
      "keys": [
        [
          "RELA3"
        ]
      ]
    },
    {
      "elementId": "ENTI3",
      "name": {
        "de": "Stern",
        "en": "Star"
      },
      "synonyms": [
        "astronomisches Objekt",
        "Sonne"
      ],
      "shortDescr": {
        "de": "Am Himmel sichtbarer, selbstleuchtender Gasball. (Stern, Sonne)",
        "en": "Self-luminous ball of gas visible in the sky. (star, sun)"
      },
      "examples": [
        "Sonne",
        "Polarstern",
        "Ursae Minoris",
        "LHS 1140",
        "Proxima Centauri",
        "Kepler-186"
      ],
      "attributes": [
        {
          "elementId": "ATTR18",
          "name": "Bezeichnung",
          "mandatory": False,
          "domainId": "DOMA23",
          "displaySeq": 1,
          "description": "Bezeichnung gem\u00e4ss Henry-Draper-Katalog (HD-Katalog)",
          "shortDescr": "Bezeichnung des Sterns im Katalog",
          "examples": [
            "HD 209458"
          ],
          "descriptive": True,
          "repeated": True
        },
        {
          "elementId": "ATTR19",
          "name": "Durchmesser",
          "mandatory": False,
          "domainId": "DOMA2",
          "displaySeq": 5,
          "description": "Der Durchmesser kann in 3 Werten angegeben werden. (Pol-, \u00c4quator- und mittlerer Durchmesser)",
          "shortDescr": "Durchmesser eines Sterns",
          "examples": [
            "3000 km",
            "15000 km",
            "12412 - 12472 km"
          ]
        },
        {
          "elementId": "ATTR20",
          "name": "Entdeckungsjahr",
          "mandatory": False,
          "domainId": "DOMA3",
          "displaySeq": 6,
          "description": "Jahr, in dem dieser Stern entdeckt wurde.",
          "examples": [
            "1752",
            "512 vuz",
            "2009"
          ]
        },
        {
          "elementId": "ATTR21",
          "name": "Entfernung",
          "mandatory": False,
          "domainId": "DOMA1",
          "displaySeq": 4,
          "description": "Distanz in Lichtjahren",
          "shortDescr": "Distanz eines Sterns von unserer Sonne",
          "examples": [
            "1.3 Mio LJ",
            "365 lj"
          ],
          "descriptive": True
        },
        {
          "elementId": "ATTR22",
          "name": "Leuchtklasse",
          "mandatory": False,
          "domainId": "DOMA26",
          "displaySeq": 3,
          "description": "Die\u00a0Leuchtkraftklasse\u00a0eines Sterns ist durch Eigenschaften bestimmt, die von seiner\u00a0Leuchtkraft\u00a0abh\u00e4ngen; dies sind insbesondere die\u00a0Breite\u00a0und die St\u00e4rke (H\u00f6he) der\u00a0Spektrallinien. So haben Riesensterne eine geringere\u00a0Schwerebeschleunigung\u00a0in ihrer\u00a0Photosph\u00e4re\u00a0als Zwergsterne gleicher Temperatur, was eine geringere\u00a0Druckverbreiterung\u00a0der Linien bewirkt, wogegen die\u00a0Spektralklasse\u00a0Eigenschaften ber\u00fccksichtigt, die prim\u00e4r von seiner Oberfl\u00e4chentemperatur abh\u00e4ngen.\n\nQuelle: https://de.wikipedia.org/wiki/Klassifizierung_der_Sterne#Leuchtkraftklassen_(Entwicklungszustand)",
          "shortDescr": "Leuchtkraftklasse",
          "examples": [
            "I",
            "V",
            "III",
            "D"
          ],
          "descriptive": True
        },
        {
          "elementId": "ATTR23",
          "name": "Name",
          "mandatory": True,
          "domainId": "DOMA23",
          "displaySeq": 2,
          "description": "ca 500 Sterne haben eigene Namen, vergeben durch die Internationale Astronomische Union (IAU)",
          "shortDescr": "Eigenname eines Sterns",
          "examples": [
            "Alpha Centauri",
            "Beta Orionis",
            "Sol"
          ],
          "descriptive": False
        }
      ],
      "keys": [
        [
          "ATTR18"
        ]
      ]
    },
    {
      "elementId": "ENTI4",
      "name": {
        "de": "Zwergplanet",
        "en": "Dwarf planet"
      },
      "shortDescr": {
        "de": "Feste Himmelsk\u00f6rper, kleiner als Planeten",
        "en": "Solid celestial bodies, smaller than planets"
      },
      "examples": [
        "Pluto",
        "Eris",
        "Haumea",
        "Makemake"
      ],
      "attributes": [
        {
          "elementId": "ATTR24",
          "name": "Oberfl\u00e4chentyp",
          "mandatory": False,
          "domainId": "DOMA27",
          "description": "Material, das die \u00e4usserste Schicht des Himmelsk\u00f6pers bildet.",
          "shortDescr": "Zustandsform der Oberfl\u00e4che",
          "examples": [
            "Feststoff",
            "Gas",
            "Eis"
          ]
        }
      ],
      "keys": [
        [
          "RELA5"
        ]
      ]
    },
    {
      "elementId": "ENTI5",
      "name": {
        "de": "Asteroid",
        "en": "Asteroid"
      },
      "examples": [
        "Ida",
        "Eugenia",
        "Sylvia",
        "Didymos",
        "Dactyl",
        "Petit-Prince",
        "Romulus",
        "Remus"
      ],
      "attributes": [],
      "keys": [
        [
          "RELA1",
          "RELA6"
        ]
      ]
    },
    {
      "elementId": "ENTI6",
      "name": {
        "de": "Komet",
        "en": "Comet"
      },
      "shortDescr": {
        "de": "Komet im Sonnensystem",
        "en": "Comet in the solar system"
      },
      "examples": [
        "Halleyscher Komet",
        "NEOWISE (2020)",
        "67P/Churyumov-Gerasimenko"
      ],
      "attributes": [],
      "keys": [
        [
          "RELA4"
        ]
      ]
    },
    {
      "elementId": "ENTI7",
      "name": {
        "de": "Begleiter",
        "en": "Companion"
      },
      "shortDescr": {
        "de": "Irgend ein Himmelsobjekt, das uns bekannt ist und einen anderes Himmelsobjekt umkreist",
        "en": "Any celestial object that is known to us and that orbits another celestial object"
      },
      "attributes": [
        {
          "elementId": "ATTR10",
          "name": "Aphel",
          "mandatory": False,
          "domainId": "DOMA4",
          "displaySeq": 6,
          "description": "Der am weitesten enfernte Punkt einer Umlaufbahn eines Begleiters um sein Mutterobjekt\n\nDie H\u00e4lfte des l\u00e4nsten Durchmessers einer Ellipse",
          "shortDescr": "Der enternteste Punkt der Umlaufbahn eines Begleiters"
        },
        {
          "elementId": "ATTR11",
          "name": "Durchmesser",
          "mandatory": False,
          "domainId": "DOMA2",
          "displaySeq": 2,
          "description": "Der Durchmesser kann in 3 Werten angegeben werden. (Pol-, \u00c4quator- und mittlerer Durchmesser)",
          "shortDescr": "Durchmesser der Kugel eines grossen Objektes",
          "examples": [
            "6112 km"
          ],
          "descriptive": True
        },
        {
          "elementId": "ATTR12",
          "name": "Entdeckungsjahr",
          "mandatory": False,
          "domainId": "DOMA3",
          "displaySeq": 7,
          "description": "Jahr, in dem dieser Begleiter entdeckt wurde.",
          "examples": [
            "1752",
            "512 vuz",
            "2009"
          ]
        },
        {
          "elementId": "ATTR13",
          "name": "mittlerer Abstand",
          "mandatory": False,
          "domainId": "DOMA4",
          "displaySeq": 4,
          "description": "Mittlerer Abstand des Himmelsk\u00f6rpers vom Mutterobjekt. W\u00e4re der Kreisradius, wenn die Umlaufbahn kreisf\u00f6rmig w\u00e4re.",
          "examples": [
            "1 AE",
            "150Mio km",
            "386000 km"
          ],
          "descriptive": True
        },
        {
          "elementId": "ATTR14",
          "name": "Name",
          "mandatory": False,
          "domainId": "DOMA23",
          "displaySeq": 1,
          "examples": [
            "(Erd-)Mond",
            "Phobos",
            "Deimos",
            "Io",
            "Europa",
            "Ganymed",
            "Triton",
            "LHS 1140 b",
            "Proxima Centauri b",
            "Kepler-186f"
          ],
          "descriptive": True
        },
        {
          "elementId": "ATTR15",
          "name": "Perihel",
          "mandatory": False,
          "domainId": "DOMA4",
          "displaySeq": 5,
          "description": "Der n\u00e4chste Punkt der Umlaufbahn eines Begleiters um sein Mutterobjekt.\n\nDie kleine Halbachse der Ellipse",
          "shortDescr": "Der am n\u00e4chsten liegende Punkt der Umlaufbahn eines Begleiters"
        },
        {
          "elementId": "ATTR16",
          "name": "Umlaufdauer",
          "mandatory": False,
          "domainId": "DOMA5",
          "displaySeq": 3,
          "description": "Zeit die ein Begleiter braucht um das Mutterobjekt zu umkreisen. (Wert + Zeiteinheit)",
          "examples": [
            "1 Jahr",
            "23 Tage",
            "3.1 Stunden"
          ],
          "descriptive": True
        }
      ],
      "keys": [
        [
          "ATTR14"
        ]
      ]
    }
  ],
  "Relations": [
    {
      "elementId": "RELA8",
      "relationType": "SUBTYPE",
      "fwd": {
        "entityId": "ENTI7",
        "assocText": {
          "de": "ist",
          "en": "is"
        },
        "cardinality": "1",
        "mandatory": True
      },
      "bwd": {
        "entityId": "ENTI1",
        "assocText": {
          "de": "ist",
          "en": "is"
        },
        "cardinality": "1",
        "mandatory": True,
        "arcNumber": 0
      }
    },
    {
      "elementId": "RELA9",
      "relationType": "SUBTYPE",
      "fwd": {
        "entityId": "ENTI7",
        "assocText": {
          "de": "ist",
          "en": "is"
        },
        "cardinality": "1",
        "mandatory": True
      },
      "bwd": {
        "entityId": "ENTI2",
        "assocText": {
          "de": "ist",
          "en": "is"
        },
        "cardinality": "1",
        "mandatory": True,
        "arcNumber": 0
      }
    },
    {
      "elementId": "RELA10",
      "relationType": "SUBTYPE",
      "fwd": {
        "entityId": "ENTI7",
        "assocText": {
          "de": "ist",
          "en": "is"
        },
        "cardinality": "1",
        "mandatory": True
      },
      "bwd": {
        "entityId": "ENTI4",
        "assocText": {
          "de": "ist",
          "en": "is"
        },
        "cardinality": "1",
        "mandatory": True,
        "arcNumber": 0
      }
    },
    {
      "elementId": "RELA11",
      "relationType": "SUBTYPE",
      "fwd": {
        "entityId": "ENTI7",
        "assocText": {
          "de": "ist",
          "en": "is"
        },
        "cardinality": "1",
        "mandatory": True
      },
      "bwd": {
        "entityId": "ENTI5",
        "assocText": {
          "de": "ist",
          "en": "is"
        },
        "cardinality": "1",
        "mandatory": True,
        "arcNumber": 0
      }
    },
    {
      "elementId": "RELA12",
      "relationType": "SUBTYPE",
      "fwd": {
        "entityId": "ENTI7",
        "assocText": {
          "de": "ist",
          "en": "is"
        },
        "cardinality": "1",
        "mandatory": True
      },
      "bwd": {
        "entityId": "ENTI6",
        "assocText": {
          "de": "ist",
          "en": "is"
        },
        "cardinality": "1",
        "mandatory": True,
        "arcNumber": 0
      }
    },
    {
      "elementId": "RELA1",
      "relationType": "M:1",
      "fwd": {
        "entityId": "ENTI5",
        "assocText": {
          "de": "umkreist von",
          "en": "orbited by"
        },
        "cardinality": "M",
        "mandatory": False
      },
      "bwd": {
        "entityId": "ENTI5",
        "assocText": {
          "de": "umkreist",
          "en": "orbits"
        },
        "cardinality": "1",
        "mandatory": False,
        "arcNumber": 1
      },
      "examples": [
        "Remus umkreist Sylvia",
        "Romulus umkreist Sylvia"
      ]
    },
    {
      "elementId": "RELA2",
      "relationType": "M:1",
      "fwd": {
        "entityId": "ENTI2",
        "assocText": {
          "de": "umkreist von",
          "en": "orbited by"
        },
        "cardinality": "M",
        "mandatory": False
      },
      "bwd": {
        "entityId": "ENTI1",
        "assocText": {
          "de": "umkreist",
          "en": "orbits"
        },
        "cardinality": "1",
        "mandatory": False,
        "arcNumber": 1
      },
      "examples": [
        "Triton umkreisst Neptun",
        "Io umkreist Jupiter",
        "Europa umkreist Jupiter",
        "(Erd-)Mond umkreist Erde"
      ]
    },
    {
      "elementId": "RELA3",
      "relationType": "M:1",
      "fwd": {
        "entityId": "ENTI3",
        "assocText": {
          "de": "umkreist von",
          "en": "orbited by"
        },
        "cardinality": "M",
        "mandatory": False
      },
      "bwd": {
        "entityId": "ENTI2",
        "assocText": {
          "de": "umkreist",
          "en": "orbits"
        },
        "cardinality": "1",
        "mandatory": True
      },
      "examples": [
        "Erde umkreist Sonne",
        "Jupiter umrkeist Sonne",
        "LHS 1140 b umkreist LHS 1140",
        "Proxima Centauri b umkreist Proxima Centauri"
      ]
    },
    {
      "elementId": "RELA4",
      "relationType": "M:1",
      "fwd": {
        "entityId": "ENTI3",
        "assocText": {
          "de": "umkreist von",
          "en": "orbited by"
        },
        "cardinality": "M",
        "mandatory": False
      },
      "bwd": {
        "entityId": "ENTI6",
        "assocText": {
          "de": "umkreist",
          "en": "orbits"
        },
        "cardinality": "1",
        "mandatory": True
      },
      "examples": [
        "Halleyscher Komet umkreist Sonne"
      ]
    },
    {
      "elementId": "RELA5",
      "relationType": "M:1",
      "fwd": {
        "entityId": "ENTI3",
        "assocText": {
          "de": "umkreist von",
          "en": "orbited by"
        },
        "cardinality": "M",
        "mandatory": False
      },
      "bwd": {
        "entityId": "ENTI4",
        "assocText": {
          "de": "umkreist",
          "en": "orbits"
        },
        "cardinality": "1",
        "mandatory": True
      },
      "examples": [
        "Pluto umkreist Sonne"
      ]
    },
    {
      "elementId": "RELA6",
      "relationType": "M:1",
      "fwd": {
        "entityId": "ENTI3",
        "assocText": {
          "de": "umkreist von",
          "en": "orbited by"
        },
        "cardinality": "M",
        "mandatory": False
      },
      "bwd": {
        "entityId": "ENTI5",
        "assocText": {
          "de": "umkreist",
          "en": "orbits"
        },
        "cardinality": "1",
        "mandatory": False,
        "arcNumber": 1
      },
      "examples": [
        "Ida umkreist Sonne",
        "Eugenia umkreist Sonne"
      ]
    },
    {
      "elementId": "RELA7",
      "relationType": "M:1",
      "fwd": {
        "entityId": "ENTI4",
        "assocText": {
          "de": "umkreist von",
          "en": "orbited by"
        },
        "cardinality": "M",
        "mandatory": False
      },
      "bwd": {
        "entityId": "ENTI1",
        "assocText": {
          "de": "umkreist",
          "en": "orbits"
        },
        "cardinality": "1",
        "mandatory": False,
        "arcNumber": 1
      },
      "examples": [
        "Charon umkreist Pluto"
      ]
    }
  ],
  "BusinessRules": [
    {
      "elementId": "BURU3",
      "restrictedElements": [
        "ENTI5"
      ],
      "description": "Ein Asteriod umkreist immer genau einen Stern oder einen Asteroiden (aber nicht sich selbst)"
    },
    {
      "elementId": "BURU4",
      "restrictedElements": [
        "ENTI1"
      ],
      "description": "Ein Mond umkreist zwingend einen Planeten oder Zwergplaneten.",
      "rule": "Mond berehchnet"
    }
  ]
} ,
                                base_uri ="mybase.com")
        print (ttl)
        return


if __name__ == '__main__':
    unittest.main()
