import preprocessing

preClass=preprocessing.preprocess()

def test_slang():
    slang=preClass.remove("pwoliiii")
    assert slang == 'pwoli'
    return slang
def test_token():
    token=preClass.tokens(test_slang())
    assert token[0]== 'poli'