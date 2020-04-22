import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from IPython.display import display
from matplotlib.backends.backend_pdf import PdfPages


def get_all_files(path: str) -> list:
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            files.append(os.path.join(r, file))
    return files


def get_idxs_wo_first(cols) -> list:
    idxs = []
    for i in range(len(cols)):
        col = cols[i]
        if 'ruleId' in col:
            idxs.append(i)
    idxs.append(len(cols))
    idxs = idxs[1:]
    return idxs


def get_df_chunk(prev_ix, ix, frame):
    t = frame.iloc[:, prev_ix:ix]
    t.rename(columns={t.columns[0]: "rule_id"}, inplace=True)
    t.rename(columns={t.columns[1]: "answered"}, inplace=True)
    t.rename(columns={t.columns[2]: "total_fires"}, inplace=True)
    t.rename(columns={t.columns[3]: "ideal_fires"}, inplace=True)
    t['range'] = frame['range']
    return t


def get_df_reformatted(df):
    prev_idx = 0
    idxs = get_idxs_wo_first(df.columns)
    tdf = pd.DataFrame()

    for idx in idxs:
        t = get_df_chunk(prev_idx, idx, df)
        prev_idx = idx
        tdf = pd.concat([tdf, t])
    return tdf


def get_final_df(path_local: str) -> pd.DataFrame:
    files = get_all_files(path_local)
    dfs = []
    for file in files:
        df = pd.read_csv(file)
        df['range'] = file[file.rindex('t_') + 2:-4]
        dfs.append(df)

    for i in range(len(dfs)):
        df = dfs[i]
        df.rename(columns={'_couponName': "coupon_name"}, inplace=True)
        dfs[i] = df.set_index('coupon_name')

    tdfs = []
    for x in range(len(dfs)):
        tdf = get_df_reformatted(dfs[x])
        tdf['days_range#'] = x + 1
        tdf = tdf.set_index('rule_id', append=True)
        # display(tdf)
        tdfs.append(tdf)
    data = pd.concat(tdfs)

    data['ans_of_asked'] = data['answered'] / data['total_fires']
    data['ask_of_shouldve'] = data['total_fires'] / data['ideal_fires']

    final = data.reset_index()
    final = final.dropna()
    return final


def write_to_pdf(df: pd.DataFrame, out_path: str):
    coupons = set(df['coupon_name'])

    with PdfPages(out_path + '\\report_graphs.pdf') as pdf:

        for c in coupons:
            d = df[df['coupon_name'] == c]

            ax = plt.subplot(title="Coupon: " + c)

            grouped_df = d.groupby(['coupon_name', 'rule_id'])
            for key, item in grouped_df:
                d = grouped_df.get_group(key)
                lbl = "Rule " + str(d['rule_id'].iloc[0])
                ax.plot('ans_of_asked', 'ask_of_shouldve', data=d, linestyle='-', marker='o', label=lbl)

                for i, point in d.iterrows():
                    ax.text(point['ans_of_asked'] + 0.01, point['ask_of_shouldve'] + 0.01, str(point['days_range#']),
                            fontsize=16)

            chartBox = ax.get_position()
            ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), shadow=False, ncol=8)
            ax.set_position([chartBox.x0, chartBox.y0, chartBox.width * 5, chartBox.height * 5])
            ax.set_ylim(ymin=0)
            ax.set_xlim(xmin=0, xmax=1)
            ax.set_xlabel("Fraction of rules answered out of fired")
            ax.set_ylabel("Fraction of rule fires out of should have fired")
            pdf.savefig(bbox_inches='tight')
            plt.close()


def write_file(in_path: str, out_path: str):
    font = {'weight': 'normal',
            'size': 18}
    matplotlib.rc('font', **font)

    df = get_final_df(in_path)
    write_to_pdf(df, out_path)
