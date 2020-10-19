import os
if __name__ == '__main__':
    lang = 'de'
    basedirec = "/Users/stb/Documents/Projekte/"
    startfile= "/Users/stb/Documents/Projekte/FYAYC_intern/gitHub/pythonWork/pythonSource/IM_WEB/webfillallin1.py "
    os.system("python3 {} {}{}/{}.params".format(startfile,basedirec,'FYAYC_intern','ModellModell') )
    os.system("python3 {}  {}{}/{}.params".format(startfile,basedirec,'BELIINF','belimo_crm'))
    os.system("python3 {}  {}{}/{}.params".format(startfile,basedirec,'BOBTDCC','BOSCH_BT'))
    os.system("python3 {}  {}{}/{}.params".format(startfile,basedirec,'EZV','EZV_Stammdaten'))
    os.system("python3 {}  {}{}/{}.params".format(startfile,basedirec,'GEBININF','IM_GEBERIT'))
    os.system("python3 {}  {}{}/{}.params".format(startfile,basedirec,'KOMADSC','komax_IM_gesamt'))
    os.system("python3 {}  {}{}/{}.params".format(startfile,basedirec,'LEISTER','leister_im'))
    os.system("python3 {}  {}{}/{}.params".format(startfile,basedirec,'Rexroth','Rexroth'))

