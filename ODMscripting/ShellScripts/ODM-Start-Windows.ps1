#autor aro 
#**

#Aufruf
#<instdir> <basedir> <imname> <language>
param($p1, $p2, $p3, $p4)
echo `n`n

#Check Instanz und Java Version
if (-not((get-process "datamodeler64W" -ea SilentlyContinue) -eq $Null)){
	echo "***********************************************"
	echo "FEHLER: Oracle Data Modeler läuft bereits!"
	echo "***********************************************"
	echo `n`n
	echo `n`n
	exit
}
$javaver = (Get-Command java | Select-Object -ExpandProperty Version).tostring()
IF (Compare-Object $javaver.substring(0,1) "8"){
	echo "***********************************************"
	echo "FEHLER: Es ist zwingend die Java Version 8 nötig!"
	echo "Aktuelle Version: $javaver"
	echo "***********************************************"
	echo `n`n
	echo `n`n
	exit
}

echo "***********************************************"
echo "Oracle Data Modeler wird gestartet"
echo "***********************************************"
echo `n`n 

# INSTDIR: 	Da in Windows keine Eigentliche "Standard-Installation" des DataModelers stattfindet, muss das Installationsverzeichniss angegeben werden
$INSTDIR = $p1

# BASEDIR: 	Basisverzeichnis in dem sich das Verzeichnis IM befindet, in dem sich das Modell befindet.
#			Default: Verzeichnis, in dem das ODM-Script das gestartet wurde steht
$BASEDIR = $p2

#IMNAME:	wird als Name der Startdatei gesetzt
$IMNAME = $p3

#LANGUAGE: EN oder DE für die Sprache des Modelers (falls wedernoch, nimm das Original des Modelers, das sich nach der SprachEinstellung des OS richtet)
#	the language configurationfiles are in <mydir>/Software/productconfig and have the names
#	  ENdatamodeler.conf
#	  DEdatamodeler.conf
#	  datamodeler.conf
$LANGUAGE = $p4

#IMDIR 
#Verzeichnis, in dem sich das IM befindet. Wir haben als Default immer das <basedir>/IM
$IMDIR = $BASEDIR + "\IM"

#MYDIR: Verzeichnis in meiner Umgebung für die gemeinsamen Dateien des Modelers
#		Der Pfad für das Standardverzeichnis für Systemtypen im ODM zeigt dorthin.
#		Inhalt: das aktuell verwendete Verzeichnis "Konfiguration"
#		Das Konfigurationsverzeichnis des akutell zu startenden Modells (IM-Verzeichnis des Mandanten) wird nach MYDIR kopiert
#		und nach dem Aussteigen aus dem Modeler wieder zurück ins IM-Verzeichnis des Mandanten
$MYDIR = $home + "\Documents\DataModeler"

echo "IMNAME:`t`t$IMNAME"
echo "LANGUAGE:`t$LANGUAGE"
echo "BASEDIR:`t$BASEDIR"
echo "MYDIR:`t`t$MYDIR"
echo "INSTDIR:`t$INSTDIR"
echo `n`n 

#copy the appropriate languageconfiguration file into the datamodelers environment
$ODMBINDIR = "$INSTDIR\datamodeler\bin"
$ODMCONFIGFILE = "$ODMBINDIR\datamodeler.conf"
switch ($LANGUAGE)
{
	"EN" { Copy-Item -Path "$MYDIR\SprachFiles\ENdatamodeler.conf" -Destination $ODMCONFIGFILE }
	"DE" { Copy-Item -Path "$MYDIR\SprachFiles\DEdatamodeler.conf" -Destination $ODMCONFIGFILE }
	Default { Copy-Item -Path "$MYDIR\SprachFiles\datamodeler.conf" -Destination $ODMCONFIGFILE }
}


$IMDIRFiles = Get-ChildItem -Path "$IMDIR\Konfiguration\"
$MYDIRFiles = Get-ChildItem -Path "$MYDIR\Konfiguration\"
#sync the configuration directory
#** aktuell kein delete
$FileDiffs = Compare-Object -ReferenceObject $IMDIRFiles -DifferenceObject $MYDIRFiles
$FileDiffs | foreach {
	$copyParams = @{
		'Path' = $_.InputObject.FullName
	}
	if ($_.SideIndicator -eq '<=')
	{
		$copyParams.Destination = $MYDIRFiles
	}	
}

#start the modeler with the model
Start-Process -FilePath "$INSTDIR\datamodeler.exe" -ArgumentList "$IMDIR\$IMNAME.dmd"

#sync back the possibly changed configuration files
#** aktuell kein delete
$FileDiffs = Compare-Object -ReferenceObject $MYDIRFiles -DifferenceObject $IMDIRFiles
$FileDiffs | foreach {
	$copyParams = @{
		'Path' = $_.InputObject.FullName
	}
	if ($_.SideIndicator -eq '<=')
	{
		$copyParams.Destination = $IMDIRFiles
	}	
}