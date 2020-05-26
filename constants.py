# Created by Maisha Jauernig on 5/1/2020
import pandas as pd

COL_LABEL_RULE = 'Rule'
COL_LABEL_CNAME = '_couponName'
COL_LABEL_RANGE = 'range'

LABEL_FULL_RANGE = "full range"
LABEL_RID = 'ruleId'

TEX_REPORT_FILE_NAME = "report.tex"


def get_study_id(in_path: str) -> str:
    return in_path[in_path.rindex("_")+1:]


def get_date(df: pd.DataFrame) -> str:
    date = df[COL_LABEL_RANGE][0]
    if date[-1] == 't':
        s = LABEL_FULL_RANGE
    else:
        s = date[date.rindex('to_') + 3:]
    return s


def get_rid_idxs(cols: list) -> list:
    idxs = []
    for i in range(len(cols)):
        col = cols[i]
        if LABEL_RID in col:
            idxs.append(i)
    return idxs