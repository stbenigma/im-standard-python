from SSOT_infra import resettransldomain,settransldomain,transl

def test_transl():
    #default ist input
    resettransldomain()
    assert  transl("") == ""
    assert  transl("Entität") == "Entität"
    #englisch
    settransldomain("en")
    assert  transl("Entität") == "Entity"
    #französisch
    settransldomain("fr")
    assert  transl("Entität") == "Entité"
    #check specific language other than set language
    assert  transl("Entität","de") == "Entität"
    assert  transl("Entität","en") == "Entity"
    assert  transl("Entität","fr") == "Entité"
    #unbekannte Sprache defaults to en
    settransldomain("es")
    assert  transl("Entität") == "Entity"
    #de = deutsch
    settransldomain("de")
    assert  transl("Entität") == "Entität"
    #and back to default
    resettransldomain()
    assert  transl("Entität") == "Entität"
