import hashlib
import random
import numpy as np

import pandas as pd


# md5加密
def md5(s):
    m = hashlib.md5()
    m.update(s.encode('utf8'))
    return m.hexdigest()


def random_str_upper(str_len):
    li = random.sample('zyxwvutsrqponmlkjihgfedcba', str_len)
    return ''.join(li).upper()


def random_num():
    return random.randint(1000, 9999)


# 平台A销售表
use_col_A = ['货号', '商品名称', '尺码', '日期', '售卖价',
             '实收金额', '销售量_含拒退', '销售量_不含拒退']

# 平台B销售表
use_col_B = [
    '款号颜色代码', '商品名称', '尺码',
    '日期', '售卖价', '活动价', '销量']

# 商品基础信息表
good_base = ['货号', '商品名称', '品牌', '商品代码', '颜色代码', '成本',
             '季节', '商品年份']

# 库存表
stock = ['sku', '在库库存']

# sku对照表
sku_table = ['sku', '货号', '尺码']


# 生成商品基础信息表
def make_good_base_tb(gid_num):
    """
    ['货号', '商品名称', '品牌', '商品代码', '颜色代码', '成本',
        '季节', '商品年份']
    :param gid_num: 货号数量
    :return: DataFrame
    """
    # 1 商品代码
    m_id_list = []
    for _ in range(gid_num):
        m_id_list.append(random_str_upper(4))
    print(m_id_list)

    # 2 颜色代码
    c_id_list = []
    temp = []
    for _ in range(int(gid_num / 2)):
        temp.append(random_num())
    for _ in range(gid_num):
        c_id_list.append(random.choice(temp))
    print(c_id_list)


def make_platform_jd():
    """
    ['货号', '商品名称', '尺码', '日期', '售卖价',
             '实收金额', '销售量_含拒退', '销售量_不含拒退']
    :return:
    """
    good_base_tb = pd.read_excel('goods_base.xlsx')

    # 2160条
    # 日期
    date = pd.date_range(
        start='2020-1-1 00:00:00',
        end='2020-6-25 23:00:00',
        freq='H')
    print(len(date))
    # print(date)
    # 拒退量
    re_num = np.random.choice([0] * 7 + [1, 2, 3], size=len(date))
    discount = np.random.choice([1, 0.5, 0.6, 0.7, 0.8, 0.9], size=len(date))
    df = pd.DataFrame({
        '货号': np.random.choice(good_base_tb['货号'], size=len(date)),
        # '商品名称': [],
        '尺码': np.random.choice(
            ['S', 'M', 'L', 'XL', 'XXL', 'M', 'L', 'XL', 'M', 'L', 'M'],
            size=len(date)),
        '日期': date,
        '销售量_不含拒退': np.random.choice(
            [1] * 28 + [2] * 5 + [3] * 2,
            size=len(date)),
    })
    df = pd.merge(df, good_base_tb, on='货号', how='left')
    df['售卖价'] = df['成本'] * 3 - 2
    df['实收金额'] = (df['售卖价'] * discount).astype(int)
    df['销售量_含拒退'] = df['销售量_不含拒退'] + re_num
    # print(df.head())
    df = df.reindex(columns=use_col_A)

    # 输出表格
    folder = '/Users/Yi/Mirror/我的python教程/ani_prepare/data_source/jd_sales/'

    for month in df['日期'].dt.month.unique():
        print(month)
        df_temp = df[df['日期'].dt.month == month]
        with pd.ExcelWriter(
                folder + str(month) + '.xlsx',
                datetime_format="YYYY-MM-DD") as writer:
            df_temp.to_excel(writer, index=False)


def make_platform_tb():
    """
    ['款号颜色代码', '商品名称', '尺码',
     '日期', '售卖价', '活动价', '销量']
    """
    good_base_tb = pd.read_excel('goods_base.xlsx')
    good_base_tb = good_base_tb.rename(columns={'货号': '款号颜色代码'})

    # 2160条
    # 日期
    date = pd.date_range(
        start='2020-1-1 00:00:00',
        end='2020-6-25 23:00:00',
        freq='H')
    # print(date)
    discount = np.random.choice([0, 0.5, 0.6, 0.7, 0.8, 0.9], size=len(date))
    df = pd.DataFrame({
        '款号颜色代码': np.random.choice(good_base_tb['款号颜色代码'], size=len(date)),
        # '商品名称': [],
        '尺码': np.random.choice(
            ['S', 'M', 'L', 'XL', 'XXL', 'M', 'L', 'XL', 'M', 'L', 'M'],
            size=len(date)),
        '日期': date,
        '销量': np.random.choice(
            [1] * 30 + [2] * 10 + [3] * 2 + [-1] * 2,
            size=len(date)),
    })
    df = pd.merge(df, good_base_tb, on='款号颜色代码', how='left')
    df['售卖价'] = df['成本'] * 3 - 2
    df['活动价'] = (df['售卖价'] * discount).astype(int)
    # print(df.head())

    # 输出表格
    folder = '/Users/Yi/Mirror/我的python教程/ani_prepare/data_source/tb_sales/'

    df = df.reindex(columns=use_col_B)
    for month in df['日期'].dt.month.unique():
        print(month)
        df_temp = df[df['日期'].dt.month == month]
        with pd.ExcelWriter(
                folder + str(month) + '.xlsx',
                datetime_format="YYYY-MM-DD") as writer:
            df_temp.to_excel(writer, index=False)


if __name__ == '__main__':
    # make_good_base_tb(10)
    make_platform_jd()
    make_platform_tb()
