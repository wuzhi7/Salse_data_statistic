import pandas as pd
import numpy as np

from generic.ufunc import v_concat_tables

jd_field = ['货号', '商品名称', '尺码', '日期', '售卖价', '实收金额', '销售量_含拒退', '销售量_不含拒退']
tb_field = ['款号颜色代码', '商品名称', '尺码', '日期', '售卖价', '活动价', '销量']
unify_field = ['货号', '尺码', '日期', '标价', '实收金额', '销量', '退货', '退货金额', '平台']

def unify_jd() -> pd.DataFrame:
    df = v_concat_tables('/Users/liyangbin/PycharmProjects/Sales/data_source/jd_sales')
    df = df.rename(columns={
        '售卖价': '标价',
        '销售量_不含拒退': '销量'
    })
    # df['退货'] = df['销售量_含拒退'] - df['销售量_不含拒退']
    df['退货'] = df['销售量_含拒退'].sub(df['销量'], fill_value=0) # 空值填充为0
    df['退货金额'] = df['实收金额']
    df['平台'] = '京东'

    df = df.reindex(columns=unify_field)    # 按照指定的列名输出数据
    return df

def unify_tb() -> pd.DataFrame:
    df = v_concat_tables('/Users/liyangbin/PycharmProjects/Sales/data_source/tb_sales')
    df = df.rename(columns={
        '款号颜色代码': '货号',
        '售卖价': '标价',

    })
    df['退货'] = np.where(df['销量'] < 0, abs(df['销量']), 0)
    df['销量'] = np.where(df['销量'] >= 0, df['销量'], 0) # 定义的'销量'这一列必须放在'退货'之后，否则，退货的数量全部为0

    df['实收金额'] = np.where(df['活动价'] > 0, df['活动价'], df['标价'])
    df['平台'] = '淘宝'
    df['退货金额'] = df['实收金额']

    df = df.reindex(columns=unify_field)    # 按照指定的列名输出数据（选择哪些列输出）
    return df

if __name__ == '__main__':
    df = unify_jd()
    df.to_excel('js.xlsx')
    df1 = unify_tb()
    df1.to_excel('tb.xlsx')