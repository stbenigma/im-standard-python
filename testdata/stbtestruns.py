from pathlib import Path

# %%

debugpath = Path.home() / "Downloads"  # try local debug path

# odm
if False:
    from LOAD_MODELS.LOAD_ODM import fillDB
    import os

    # BOBT
    if True:
        model = "Bosch_BT_ENG"
        modeldir = "/Users/stb/Documents/Projekte/BOBTDCC/IM"
        destdir = "/Users/stb/Documents/Projekte/BOBTDCC/newModelQ42023"
        dbfile = destdir + f"/{model}.db"
    elif False:
        model = "xy"
        modeldir = "/Users/stb/Documents/Projekte/xx/IM"
        destdir = "/Users/stb/Documents/Projekte/xx/newModelQ42023"
        dbfile = destdir + f"/{model}.db"

    if os.path.exists(dbfile):
        os.remove(dbfile)
    db = fillDB.fillmergedb(pmodelname=model,
                            pdbfilepath=destdir + "/" + model + ".db",
                            pmodelfilepath=modeldir + "/" + model + ".dmd",
                            pmodellang="de"
                            , plogfilepath=destdir + "/" + model + ".log", pverbose=True)

# dataspot Bossard
if False:
    from LOAD_MODELS.LOAD_DATASPOT import DSAccess, DSTenant

    fyaycrepo = 'https://partner.dataspot.io'
    fyaycrepodb = "foryouandyourcustomers"
    fyayctenantname = "foryouandyourcustomers"
    dstenantname = "Basis - Schwipsti GmbH"
    bossardtenantname = "Bossard"
    bossardDS = "/Users/stb/Documents/Projekte/Bossard/dataspot"

    dsaccess = DSAccess(repository=fyaycrepo, repoowner=fyaycrepodb,
                        tenantname=bossardtenantname, viaazure=True)
    tenant = DSTenant(lang="de", dsaccess=dsaccess)
    readjson = JSModel(pmodel=tenant.spodjson(), pwithversioncheck=False)
    readjson.write_json(bossardDS + "/bossarddataspot.json")
    createJSON.createJSON(pfilepath=bossardDS, pfilename="bossard.json")

# miro
if False:
    # BOBT
    if False:
        from LOAD_MODELS.LOAD_MIRO import miromodel
        from SSOT_db.IM_JSON import JSModel

        mirotestboardname = "SPOD Test Board"
        baarcredentials = Path.home() / ".miro" / "credentials-mirobaar.yaml"
        testcredentials = Path.home() / ".miro" / "credentials-mirodev.yaml"

        if True:
            boardname = "Miro API Test"
            # boardname="MDM-TM-Governance"
            print("".join("=" for i in range(60)))
            miromodel.listboards(credentialfile=baarcredentials, boardname=boardname)
            print("".join("=" for i in range(60)))
            miromodel.listframes(credentialfile=baarcredentials, boardname=boardname)
            print("".join("=" for i in range(60)))

            if False:
                miromodel.miroframe2json(credentialfile=baarcredentials, jsonfile=debugpath / "BayWa.json",
                                         framename="Workshop 8/8 - finales Ergebnis",
                                         lang="de", boardname=boardname)
            if True:
                destdir = "/Users/stb/Documents/Projekte/BOBTDCC/newModelQ42023"
                dbfile = destdir + "/Bosch_BT.db"
                jsonfile = destdir + "/Bosch_BT.json"
                jsonfileupd = destdir + "/Bosch_BTUPD.json"
                dbfile = destdir + "/Bosch_BT_ENG.db"
                jsonfile = destdir + "/Bosch_BT_ENG.json"
                jsonfileupd = destdir + "/Bosch_BTUPD_ENG.json"

                miromodel.diagram2miro(credentialfile=baarcredentials, boardname=boardname,
                                       destjsonfile=jsonfileupd, jsonfile=jsonfile,
                                       diagramname="BT-Organization_en"
                                       )

    # BayWa
    if True:
        from LOAD_MODELS.LOAD_MIRO import miromodel
        from SSOT_db.IM_JSON import JSModel
        from LOAD_MODELS.LOAD_INFRA import mergedbs
        from PUBLISH_MODEL.diagrams import diagramgeneration

        baarcredentials = Path.home() / ".miro" / "credentials-mirobaar.yaml"
        testcredentials = Path.home() / ".miro" / "credentials-mirodev.yaml"
        destdir = "/Users/stb/Documents/Projekte/BayWa/"
        dbfile = destdir + "/BayWa.db"
        jsonfile = destdir + "/BayWa.json"
        mirojsonfile = destdir + "/BayWa.miro.json"
        framename = "Workshop 8/8-0"

        if True:
            boardname = "Miro API Test"
            # boardname="MDM-TM-Governance"
            print("".join("=" for i in range(60)))
            miromodel.listboards(credentialfile=baarcredentials, boardname=boardname)
            print("".join("=" for i in range(60)))
            miromodel.listframes(credentialfile=baarcredentials, boardname=boardname)
            print("".join("=" for i in range(60)))

            if True:
                miromodel.miroframe2json(credentialfile=baarcredentials,
                                         jsonfile=mirojsonfile, framename=framename,
                                         lang="de", boardname=boardname, checkjsonfile=True)
                jsonmodel = JSModel.readfromfile(mirojsonfile)
                jsonmodel.jsmodel = mergedbs.jsonviadbtojson(pmodel=jsonmodel,
                                                             psrcname="MIRO")
                jsonmodel.write_json(jsonfile)

                diagramgeneration.main(psysargs=['stbtestruns.py',
                                                 f'--name={framename}',
                                                 '/Users/stb/Documents/Projekte/BayWa/Baywa.json'
                                                 ])
                # listWebdoku.webmain(pjsonfilepath=mirojsonfile, pwebdirec=destdir,
                #                     pmodelname="BayWa", pfiletype="html", singlefile=True,
                #                     diagtype="FYAYC")

            if False:
                miromodel.diagram2miro(credentialfile=baarcredentials, boardname=boardname,
                                       jsonfile=jsonfile,
                                       diagramname="Workshop 8/8"
                                       )

# semAnalyse
if True:
    from SSOT_db.IM_JSON import JSModel,readjsonfile
    from SSOT_infra import nvl
    if False:

        def terms(model: JSModel):
            names = [val["name"][model.getdefaultlang()]
                     for key, val in model.getelements("entities").items()]
            names.extend([val["name"][model.getdefaultlang()]
                          for key, val in model.getelements("attributes").items()])
            names = list(set(names))
            return [{"term": name, "generic": None, "type": None, "problSynoms": None}
                    for name in names]


        def verbs(model):
            verbs = [val["from-to"]["assoc"][model.getdefaultlang()]
                     for key, val in model.getelements("relations").items()]
            verbs.extend([val["to-from"]["assoc"][model.getdefaultlang()]
                          for key, val in model.getelements("relations").items()])
            verbs = list(set(verbs))
            return [{"verb": verb, "generic": None, "problSynoms": None} for verb in verbs]

        repis = lambda s: 'is' if s is None or s=="" else s
        def facts(model):
            relas = [model.getbyid(rela["from-to"]["enti"])["name"][model.getdefaultlang()]+
                 " "+
                repis(rela["from-to"]["assoc"][model.getdefaultlang()]) +
                 " "+
                model.getbyid(rela["to-from"]["enti"])["name"][model.getdefaultlang()]
                for rela in model.getelements("relations").values()]
            relas.extend([model.getbyid(rela["to-from"]["enti"])["name"][model.getdefaultlang()] +
                 " "+
                repis(rela["to-from"]["assoc"][model.getdefaultlang()]) +
                 " "+
                model.getbyid(rela["from-to"]["enti"])["name"][model.getdefaultlang()]
                for rela in model.getelements("relations").values()]
                )
            relas = list(set(relas))
            return [{"fact": rela, "generic": None, "significance": None, }
                    for rela in relas]

        # teste semantische Analse
        model = JSModel.readfromfile(pwithcheck=False,
                                     pfilename="/Users/stb/Downloads/ModellModell_neu.json")

        testjson = JSModel(pwithversioncheck=False,
                           pmodel=
                           {
                               "project": "ModellModell",
                               "public": True,
                               "owner": "foryouandyourcustomers AG",
                               "context": """""",
                               "origin": "internes metamodell ModellModell_neu",
                               "rating": [
                                   {"generic": "1: very generic, highly interpretable - 5:  very concret, clear"},
                                   {"significance": "1: meaningless, senseless - 5: very meaningful, significant"},
                                   {"type": "T(hing), A(ttribute), B(both)"},
                                   {
                                       "problSynoms": "List of probable synonyms for this term/verb in the list of all terms/verbs "}
                               ],
                               "terms": terms(model),
                               "verbs": verbs(model),
                               "facts": facts(model)
                           }
                           )
        testjson.write_json(destination="/Users/stb/Downloads/checkmodmod.json")

        model = JSModel.readfromfile(pwithcheck=False,
                                     pfilename="/Users/stb/Downloads/BayWa.json")

        testjson = JSModel(pwithversioncheck=False,
                           pmodel=
                           {
                               "project": "BayWa",
                               "public": False,
                               "owner": "BayWa",
                               "context": """""",
                               "origin": "Modellbeispiel von BayWa",
                               "rating": [
                                   {"generic": "1: very generic, highly interpretable - 5:  very concret, clear"},
                                   {"significance": "1: meaningless, senseless - 5: very meaningful, significant"},
                                   {"type": "T(hing), A(ttribute), B(both)"},
                                   {"problSynoms": "List of probable synonyms for this term/verb in the list of all terms/verbs "}
                                   ],
                               "terms": terms(model),
                               "verbs": verbs(model),
                               "facts": facts(model)
                           }
                           )
        testjson.write_json(destination="/Users/stb/Downloads/checkbaywa.json")
    if True:
        def printresults(name,result):
            print (name)
            facts = dict()
            verbs = dict()

            terms = dict()

            generics= [f["generic"] for f in result["facts"]]
            facts["generic"]=round(sum(generics)/len(generics),1) if len(generics) > 0 else 0
            generics= [f["significance"] for f in result["facts"]]
            facts["significance"]=round(sum(generics)/len(generics),1) if len(generics) > 0 else 0
            print ("facts",facts)

            generics= [f["generic"] for f in result["terms"]]
            terms["generic"]=round(sum(generics)/len(generics),1) if len(generics) > 0 else 0
            synos= [len(f["problSynoms"]) for f in result["terms"]]
            terms["synonym"]=round(sum(synos)/len(synos),1) if len(synos) > 0 else 0
            print ("terms",terms)

            generics= [f["generic"] for f in result["verbs"]]
            verbs["generic"]=round(sum(generics)/len(generics),1) if len(generics) > 0 else 0
            synos= [len(f["problSynoms"]) for f in result["verbs"]]
            verbs["synonym"]=round(sum(synos)/len(synos),1) if len(synos) > 0 else 0
            print ("verbs",verbs)
            return

        #printresults("BayWa_chtGPT.json",readjsonfile("/Users/stb/Downloads/BayWa_chtGPT.json"))
        #printresults("simpletest-chatGPT-2.txt",readjsonfile("/Users/stb/Downloads/simpletest-chatGPT-2.txt"))
        printresults("semGrp1",readjsonfile("/Users/stb/Downloads/semGrp1-2.txt"))

