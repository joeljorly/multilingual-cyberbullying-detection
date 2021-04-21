import filtering

newClass=filtering.Filter()

def test_emoji():
    emoji=newClass.remove_emoji("Ente amooo samadhanam aayi❤️,😁😂😂😂😂")
    assert emoji=="Ente amooo samadhanam aayi , "
    return emoji

def test_pattern():
    pattern=newClass.pattern(test_emoji())
    assert pattern=="Ente amooo samadhanam aayi "
    return pattern

def test_remove():
    remove=newClass.remove(test_pattern())
    if remove is None:
        assert remove is None
    
