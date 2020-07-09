from WebReport import webfillallin1

if __name__ == '__main__':
    lang = 'de'
    basedirec = "/Users/stb/Documents/Projekte/"
    webfillallin1.main(pdirec="{}{}/{}.params".format(basedirec,'FYAYC_intern','ModellModell'),plang='de')
    webfillallin1.main(pdirec="{}{}/{}.params".format(basedirec,'BELIINF','belimo_crm'),plang='de')
    webfillallin1.main(pdirec="{}{}/{}.params".format(basedirec,'BOBTDCC','BOSCH_BT'),plang='de')
    webfillallin1.main(pdirec="{}{}/{}.params".format(basedirec,'EZV','EZV_Stammdaten'),plang='de')
    webfillallin1.main(pdirec="{}{}/{}.params".format(basedirec,'GEBININF','IM_GEBERIT'),plang='de')
    webfillallin1.main(pdirec="{}{}/{}.params".format(basedirec,'KOMADSC','komax_IM_gesamt'),plang='de')
    webfillallin1.main(pdirec="{}{}/{}.params".format(basedirec,'LEISTER','leister_im'),plang='de')
    webfillallin1.main(pdirec="{}{}/{}.params".format(basedirec,'Rexroth','Rexroth'),plang='de')
    webfillallin1.main(pdirec="{}{}/{}.params".format(basedirec,'',''),plang='de')

