import pandas as pd
import os


# 定义一个函数，上下合并表格
def v_concat_tables(folder) -> pd.DataFrame:
    df_list = []  # 一个空的数据列表
    for fn in os.listdir(folder):  # 遍历一个文件夹中的所有文件

        afn = os.path.join(folder, fn)  # 定义一个绝对路径
        #         print(afn)
        df_temp = pd.read_excel(afn)  # 读取每一个Excel文件
        df_list.append(df_temp)  # 把每一个读取的文件添加到空的列表中
    df = pd.concat(df_list, ignore_index=True)  # 上下拼接所有列表，形成一个dataframe
    # print(df)
    return df

if __name__ == '__main__':
    df_jd = v_concat_tables('/Users/liyangbin/PycharmProjects/Sales/data_source/jd_sales')
    df_jd.to_excel('jd_sales.xlsx')