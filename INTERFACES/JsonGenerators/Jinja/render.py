import json
from jinja2 import Environment, FileSystemLoader

env = Environment(
    loader=FileSystemLoader("/home/claude/dmp_jinja"),
    trim_blocks=True,
    lstrip_blocks=True,
    keep_trailing_newline=True,
)
tpl = env.get_template("dmp_template.j2")

context = {
    "dmpId": "urn:uuid:1a2b3c4d-0001-4a00-8000-000000000001",
    "createdAt": "2026-07-14T10:00:00Z",
    "version": "1.0",
    "nameplate": {
        "materialId": "urn:uuid:92ef6f0b-a04b-4830-9968-f25f21273fc1",
        "companyName": "Chemical Company GmbH",
        "productId": "A1234",
        "tradeProductIdentifier": "4101234560011",
        "productName": "SuperFibramide",
        "granularity": "batch",
        "batchId": "B-2026-0042",
    },
    "components": [
        {
            "id": "unpacked-product",
            "type": "unpackaged_product",
            "granularity": "batch",
            "materialDeclaration": {
                "compositionType": "mixture",
                "mixture": {
                    "mixtureNames": [
                        {"text": "SuperFibramide Compound", "language": "en"},
                        {"text": "SuperFibramide Verbindung", "language": "de-DE"},
                    ],
                    "asManufactured": True,
                    "euUfiNumbers": ["ABCD-1234-5678-EFGH"],
                    "mixtureHazardClassification": [
                        {
                            "code": "H315",
                            "texts": [
                                {"text": "Causes skin irritation", "language": "en"}
                            ],
                            "hazardClass": "Skin corrosion/irritation",
                            "hazardCategoryCode": "Skin Irrit. 2",
                        }
                    ],
                    "reachArt33SvhcAboveThreshold": False,
                    "constituents": [
                        {
                            "role": "main_constituent",
                            "substanceMainFunction": "polymer backbone",
                            "substance": {
                                "internationalName": "Fibramide base polymer",
                                "identifiers": {
                                    "casNumber": "1234-56-7",
                                    "trivialName": "Fibramide",
                                },
                                "regulatory": {
                                    "activeBiocide": False,
                                    "listedInAnnexVIClp": False,
                                    "nanoform": "no",
                                },
                                "hazardStatements": [
                                    {"code": "H315"}
                                ],
                                "reachArt33SvhcAboveThreshold": False,
                                # Rekursion: Verunreinigung als eingebettete Substanz
                                "impurities": [
                                    {
                                        "constituentSubstanceCategory": "residual monomer",
                                        "substance": {
                                            "identifiers": {"casNumber": "9876-54-3"},
                                            "regulatory": {},
                                        },
                                        "concentration": {
                                            "maxValue": 0.05,
                                            "maxOperator": "<",
                                            "unit": "%",
                                        },
                                    }
                                ],
                            },
                            "concentration": {
                                "minValue": 60,
                                "minOperator": ">=",
                                "maxValue": 70,
                                "maxOperator": "<=",
                                "unit": "%",
                            },
                        },
                        {
                            "role": "additive",
                            "substance": {
                                "identifiers": {"casNumber": "111-22-3"},
                                "regulatory": {},
                            },
                            "concentration": {"exactValue": 2.5, "unit": "%"},
                        },
                    ],
                },
                "safeUseInformation": {
                    "identifiedUses": ["industrial fibre production"],
                    "productLabellingInformationClp": {
                        "signalWord": "Warning",
                        "hazardPictograms": ["GHS07"],
                        "precautionaryStatements": ["P210", "P260"],
                    },
                },
            },
            "sustainability": {
                "sustainabilityGeneral": {
                    "sustainabilityDeclaredUnitMeasurement": "kg",
                    "sustainabilityProductMassPerDeclaredUnit": 1.0,
                    "sustainabilityDeclaredUnitAmount": 1.0,
                },
                "impactCategories": {
                    "productCarbonFootprint": {
                        "pcfId": "urn:uuid:2b2b3c4d-0002-4a00-8000-000000000002",
                        "pcfVersion": 1,
                        "pcfDateOfIssue": "2026-06-01",
                        "pcfValidityPeriod": {"start": "2026-06-01", "end": "2027-06-01"},
                        "pcfStatus": "Active",
                        "pcfGeography": {"regionOrSubregion": "Western Europe", "country": "DE"},
                        "pcfReferencePeriod": {"start": "2025-01-01", "end": "2025-12-31"},
                        "pcfCrossSectoralStandards": ["ISO 14067:2018"],
                        "pcfProductOrSectorSpecificRules": [],
                        "pcfPrimaryDataShare": 80,
                        "pcfSecondaryEmissionFactorSources": ["ecoinvent 3.10"],
                        "pcfExemptedEmissionsPercent": 1.5,
                        "pcfPartialFull": "cradle-to-gate",
                        "pcfCharacterizationFactors": "AR6",
                        "ccsCapturing": {"value": 0, "uom": "kg"},
                        "ccsTechnologicalCO2CaptureIncluded": False,
                        "ccuCalculationApproach": "not-applicable",
                        "ccuCo2Origin": "not applicable",
                        "ccuCarbonContent": {"value": 0, "uom": "kg"},
                        "ccuCreditCertificateScheme": "",
                        "useCredit": {"value": 0, "uom": "kg"},
                        "useCreditCertificateScheme": "",
                        "freeAttributionInMassBalancing": False,
                        "massBalancingCertificateScheme": "",
                        "massBalancingUsed": False,
                        "massBalancingCalculationApproach": "not applicable",
                        "allocationInForeground": {
                            "pcfAllocationWasteIncineration": "Cut-off",
                            "pcfAllocationRecycledCarbon": "Not-applicable",
                        },
                        "carbonContent": {
                            "pcfCarbonContentTotal": {"value": 0.49, "uom": "kg"},
                            "pcfBiogenicCarbonContent": {"value": 0.0, "uom": "kg"},
                        },
                        "lifeCycleStagesAndEmissions": {
                            "productionStage": {
                                "pcfIncludingBiogenicUptake": {"value": 1.2, "uom": "kg"},
                                "pcfExcludingBiogenicUptake": {"value": 1.2, "uom": "kg"},
                                "pcfAircraftGhgEmissions": {"value": 0.0, "uom": "kg"},
                            }
                        },
                    }
                },
            },
            "certificatesOfAnalysis": {
                "document": {
                    "uri": "https://example.com/coa/12345.pdf",
                    "contentType": "application/pdf",
                    "checksum": {
                        "algorithm": "SHA-256",
                        "value": "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
                    },
                },
                "reference": {"coaNumber": "COA-2026-0042"},
                "dates": {"dateOfIssue": "2026-06-01"},
            },
        },
        {
            "id": "packaging",
            "type": "packaging component",
            "granularity": "model",
        },
    ],
}

rendered = tpl.render(**context)

# JSON-Parse-Check
try:
    parsed = json.loads(rendered)
except json.JSONDecodeError as e:
    print("JSON PARSE ERROR:", e)
    print(rendered)
    raise SystemExit(1)

with open("/home/claude/dmp_jinja/rendered_example.json", "w") as f:
    json.dump(parsed, f, indent=2, ensure_ascii=False)

print("OK - valides JSON erzeugt, gespeichert unter rendered_example.json")
