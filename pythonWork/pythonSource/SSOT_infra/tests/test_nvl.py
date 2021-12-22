from SSOT_infra import nvl,nvl2

def test_nvl():
    assert nvl(None,1) == 1
    assert nvl(77,1) == 77
    assert nvl('abc','x') == 'abc'
    assert nvl('abc') == 'abc'
    assert nvl(None) == ''

def test_nvl2():
    assert nvl2(None,1,2) == 1
    assert nvl2(None,1,'a2') == 1
    assert nvl2(None,'x',1) == 'x'
    assert nvl2(11,1,2) == 2
    assert nvl2(None,None,None) == None
    assert nvl2([],None,None) == None
    assert nvl2('abc','None','NotNone') == 'NotNone'
    assert nvl2('','None','NotNone') == 'NotNone'
