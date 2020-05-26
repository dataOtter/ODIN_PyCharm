# Created by Maisha Jauernig at 5/1/2020
import typing

import pandas as pd
import os

import constants


def get_rule_cols(df: pd.DataFrame) -> list:
    to_return = []
    cols = df.columns
    for i in range(len(cols)):
        c = cols[i]
        if constants.COL_LABEL_RULE in c or constants.COL_LABEL_CNAME in c:
            to_return.append(i)
    return to_return


def get_all_files(path_local: str) -> list:
    files_local = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path_local):
        for file in f:
            files_local.append(os.path.join(r, file))
        break
    return files_local


def get_rule_dfs(in_path: str, drop_full_duration: bool=False) -> typing.List[pd.DataFrame]:
    files = get_all_files(in_path)
    dfs = []

    for file in files:
        df = pd.read_csv(file)
        cols = get_rule_cols(df)
        df = df.iloc[:, cols]

        if drop_full_duration and file[-5:-4] == 't':  # full duration short_report.csv
            continue
        df['range'] = file[file.rindex('t_') + 2:-4]
        #df.rename(columns={'_couponName': "coupon_name"}, inplace=True)
        dfs.append(df)

    return dfs
