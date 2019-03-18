# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 09:55:26 2019

@author: hehe
"""

'''
商铺数据加载及存储
'''
#导入模块
import pandas as pd



'''
(1)读取数据
'''
f=open('C:\\Users\\hehe\\Desktop\\practices\\商铺数据加载及存储\\input\\data.csv','r',encoding='utf-8')
data=pd.read_csv(f)

'''
(2）数据清洗
函数式编程，创建清洗函数
comment\price\commentlist
'''
def fcm(s):
    if '条' in s:
        return int(s.split(' ')[0])
    else:
        return '缺失数据'

def fpr(s):
    if '￥' in s:
        return float(s.split('￥')[-1])
    else:
        return '缺失数据'
    
def fcl(s):
    if ' ' in s:
        quality = float(s.split('                                ')[0][2:])
        environment = float(s.split('                                ')[1][2:])
        service = float(s.split('                                ')[2][2:-1])
        return [quality,environment,service]
    else:
        return '缺失数据'
    
# 数据清洗

datalst = []  # 创建空列表

f.seek(0)
n = 0  # 创建计数变量
for i in f.readlines()[1:20]:
    data = i.split(',')
    #print(data)
    classify = data[0]             # 提取分类
    name = data[1]                 # 提取店铺名称
    comment_count = fcm(data[2])   # 提取评论数量
    star = data[3]                 # 提取星级
    price = fpr(data[4])           # 提取人均
    add = data[5]                  # 提取地址
    qua = fcl(data[6])[0]          # 提取质量评分
    env = fcl(data[6])[1]          # 提取环境评分
    ser = fcl(data[6])[2]          # 提取服务评分
    if  '缺失数据' not in [comment_count, price, qua]:   # 用于判断是否有数据缺失
        n += 1
        data_re = [['classify',classify],
                  ['name',name],
                  ['comment_count',comment_count],
                  ['star',star],
                  ['price',price],
                  ['address',add],
                  ['quality',qua],
                  ['environment',env],
                  ['service',ser]]
        datalst.append(dict(data_re))   # 生成字典，并存入列表datalst
        print('成功加载%i条数据' %n)
    else:
        continue
    
print(datalst) 
print('总共加载%i条数据' %n)

# 数据存储.pkl数据

import pickle
pic = open('C:/Users/Hjx/Desktop/data.pkl','wb')
pickle.dump(datalst,pic)
pic.close()
print('finished!')
# 将数据存成了pkl文件
