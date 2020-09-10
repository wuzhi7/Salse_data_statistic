from datetime import date
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from generic.ufunc import insert_img_to_excel
from tasks.unify_tables import unify_jd, unify_tb

# 1）下载数据源
def download_data_source():
    print('下载数据源')

# 2）输出数据总表
def out_all_sales():
    df_jd = unify_jd()
    df_tb = unify_tb()
    # 合并销售总表
    df = pd.concat([df_jd, df_tb], ignore_index=True)

    # 读取其它表格并筛选数据
    df_goods_base = pd.read_excel('/Users/liyangbin/PycharmProjects/Sales/data_source/goods_base.xlsx')

    df_cost_other = pd.read_excel('/Users/liyangbin/PycharmProjects/Sales/data_source/cost_other.xlsx')
    df_cost_platform = pd.read_excel('/Users/liyangbin/PycharmProjects/Sales/data_source/cost_platform.xlsx')
    df_cost_platform = df_cost_platform[df_cost_platform['备注'] == '常规'] # 筛选数据
    df_cost_platform = df_cost_platform[['平台', '扣点']]   # 选择指定的列
    # 连接各表格
    df = pd.merge(df, df_goods_base, how='left', on='货号', validate='m:1')
    df = pd.merge(df, df_cost_other, how='left', on='季节', validate='m:1')
    df = pd.merge(df, df_cost_platform, how='left', on='平台', validate='m:1')

    # 数据优化
    df.loc[(df['平台'] == '京东') & (df['日期'].dt.date >= date(2020, 6, 10))
           & (df['日期'].dt.date <= date(2020, 6, 20)), '扣点'] = 0.12      # 修改指定条件的数据

    # 生成计算后的列
    df['收入'] = df['实收金额'] * df['销量'] - df['退货'] * df['退货金额']
    df['利润'] = df['收入'] * (1 - df['扣点']) - df['成本'] * df['销量'] - \
               (df['上架费'] + df['包装费'] + df['物流费']) * (df['销量'] + df['退货'])


    df.to_excel('/Users/liyangbin/PycharmProjects/Sales/data_out/all_data.xlsx', index=False)
    df.to_pickle('/Users/liyangbin/PycharmProjects/Sales/data_out/all_data.pkl')

# 3）输出统计数据1
def out_statistics_1():
    df = pd.read_excel('/Users/liyangbin/PycharmProjects/Sales/data_out/all_data.xlsx')
    df = pd.pivot_table(df, index='货号', values=['销量', '实收金额', '收入', '利润'],
                        aggfunc=sum).reset_index()  #.reset_index()把'货号'那一列设置为行索引
    df = df.reindex(columns=['货号', '图片', '销量', '实收金额', '收入', '利润']) #重新设置列名


    afn= '/Users/liyangbin/PycharmProjects/Sales/data_out/good_id_statistics.xlsx'
    df.to_excel(afn, index=False)
    insert_img_to_excel(afn, 'A', 'B', '/Users/liyangbin/PycharmProjects/Sales/data_source/goods_image')

# 4）输出统计数据2
def out_statistics_2():
    df = pd.read_pickle('/Users/liyangbin/PycharmProjects/Sales/data_out/all_data.pkl')

    sns.set(context='talk', style='darkgrid', palette='pastel', rc={'figure.figsize': [15, 10]})
    plt.rcParams['font.sans-serif'] = ['Hiragino Sans GB']
    plt.rcParams['axes.unicode_minus'] = False

    df['月份'] = df['日期'].dt.month
    sns.barplot(x='月份', y='销量', hue='平台', data=df, estimator=sum, ci=None)
    plt.savefig('/Users/liyangbin/PycharmProjects/Sales/data_out/月份_销量.png', dpi=150)

if __name__ == '__main__':
    # out_all_sales()
    # out_statistics_1()
    out_statistics_2()