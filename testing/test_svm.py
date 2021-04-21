import svm_with_dia_reduction

svm=svm_with_dia_reduction.dia_red()

def test_predict():
    predict=svm.red(['poda patti'])
    assert predict=='bullying'