import os
import pandas as pd

path = "D:\\eclipse projects\\ODIN_data\\tex_study_34"


def get_all_files(path_local: str) -> list:
    files_local = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path_local):
        for file in f:
            files_local.append(os.path.join(r, file))
    return files_local


def get_title() -> str:
    return "\\documentclass[landscape]{article} \\usepackage[utf8]{inputenc} \\usepackage{multirow} \
\\usepackage[table]{xcolor} \\usepackage[margin=0.5in]{geometry} \n \\title{Daily Report for Study: XYZ} \
\\author{maisha.jauernig } \\begin{document} \\maketitle \\newpage \n\n"


def get_col(num_cols: int, rids: list) -> str:
    table_local = "\\begin{tabular}{"
    for i in range(num_cols):
        table_local += "|c"
    table_local += "|} \\hline \\multirow{2}{*}{coupon} "

    for i in rids:
        table_local += "& \\multicolumn{" + str(num_subcols) + "}{c|}{Rule " + str(i) + "}"
    table_local += "\\\\ \\cline{2-" + str(num_cols) + "} \n"

    for i in range(len(rids)):
        table_local += " & answered/fired & fired/ideal fires & ideal fires "
    table_local += "\\\\ \\hline \\hline \n"

    return table_local


def get_row(df_local: pd.DataFrame, df_col_idx_local: int, num_cols: int) -> str:
    table_local = ""
    for r in range(len(df_local)):
        table_local += df_local.iloc[r]['coupon_name']

        for i in range(df_col_idx_local, df_col_idx_local + num_cols, 4):
            ans = df_local.iloc[r, i]
            fired = df_local.iloc[r, i + 1]
            ideal = df_local.iloc[r, i + 2]
            ans_of_fired = ans / fired if fired > 0 else 0
            fir_of_ideal = fired / ideal if ideal > 0 else 0
            table_local += " & " + (" \\cellcolor{red!25} " if ans_of_fired < .5 else " ") \
                           + str(ans_of_fired) + " & " + (" \\cellcolor{red!25} " if fir_of_ideal < .5 else " ") \
                           + str(fir_of_ideal) + " & " + str(ideal)

        table_local += "\\\\ \\hline \n"

    return table_local


def get_one_table_page(df_local: pd.DataFrame, all_rids_local: list, num_subcols_local: int,
                       df_col_idx_local: int) -> str:
    date_local = df_local['range'][0]
    date_local = date_local[date_local.rindex('to_') + 3:]

    table = "\\begin{center} {\\huge " + date_local + " \\\\ } \n"

    for rid_idx in range(0, len(all_rids_local), 2):
        rids = all_rids_local[rid_idx:rid_idx + 2]
        num_cols = len(rids) * num_subcols_local + 1

        table += get_col(num_cols, rids)
        table += get_row(df_local, df_col_idx_local, num_cols)
        table += "\\\\ \\end{tabular} \n"

        df_col_idx_local += num_cols + 1

    table += "\\end{center} \\newpage \n\n"

    return table


files = get_all_files(path)
dfs = []
for file in files:
    df = pd.read_csv(file)
    df['range'] = file[file.rindex('t_')+2:-4]
    df.rename(columns={'_couponName': "coupon_name"}, inplace = True)
    dfs.append(df)

table = get_title()

for df in dfs:
    all_rids = []
    for i in range(1, len(df.columns)-1, 4):
        all_rids.append(df.iloc[0,i])

    num_subcols = 3
    df_col_idx = 2

    date = df['range'][0]
    date = date[date.rindex('to_')+3:]

    table += get_one_table_page(df, all_rids, num_subcols, df_col_idx)

table += "\\end{document}"
#print(table)

with open("for_tex.txt", "w") as text_file:
    text_file.write(table)
