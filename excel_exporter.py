import pandas as pd
from pandas import ExcelWriter
import os.path

## convert the comments to a xlsx sheet
def export(comments):
    fname = 'data/comments.xlsx'
    temp = {}
    temp_names = []
    temp_comments = []
    if os.path.isfile(fname):
        saved = pd.read_excel(fname)
        temp_comments.extend(saved['comment'])
    temp_comments.extend(comments)
    temp.update({'comment': temp_comments})
    df = pd.DataFrame(temp)
    writer = ExcelWriter(fname)
    df.to_excel(writer, 'paul', index=False)
    writer.save()