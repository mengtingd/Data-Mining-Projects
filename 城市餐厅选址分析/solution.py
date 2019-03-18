# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 16:43:06 2019

@author: hehe
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import warnings 
warnings.filterwarnings('ignore')

from bokeh.plotting import figure,show,output_file
from bokeh.models import ColumnDataSource

'''
(1)加载数据
'''
import os
os.chdir('C:\\Users\\hehe\\Desktop\\practices\\城市餐厅选址分析\\input\\')
df1=pd.read_excel('data.xlsx',sheetname=0)

'''
(2)数据清洗
清除空值，清除口味、人均消费为0的样本
计算性价比
'''
data1=df1[['类别','口味','环境','服务','人均消费']]
data1.dropna(inplace=True)
data1=data1[(data1['口味']>0) & (data1['人均消费']>0)]
data1['性价比']=(data1['口味']+data1['环境']+data1['服务'])/data1['人均消费']

def f1():
    fig,axes=plt.subplots(1,3,figsize=(10,4))
    data1.boxplot(column=['口味'],ax=axes[0])
    data1.boxplot(column=['人均消费'],ax=axes[1])
    data1.boxplot(column=['性价比'],ax=axes[2])
#制作箱线图，查看异常值
    
def f2(data,col):
    q1=data[col].quantile(q=0.25)
    q3=data[col].quantile(q=0.75)
    iqr=q3-q1
    t1=q1-3*iqr
    t2=q3+3*iqr
    return data[(data[col]>t1)&(data[col]<t2)][['类别',col]]
#清除异常值

data_kw=f2(data1,'口味')
data_rj=f2(data1,'人均消费')
data_xj=f2(data1,'性价比')

def f3(data,col):
    col_name=col+'_norm'
    data_gp=data.groupby('类别').mean()
    data_gp[col_name]=(data_gp[col]-data_gp[col].min())/(data_gp[col].max()-data_gp[col].min())
    data_gp.sort_values(by=col_name,inplace=True,ascending=False)
    return data_gp
#标准化指标并排序

data_kw_score=f3(data_kw,'口味')
data_rj_score=f3(data_rj,'人均消费')
data_xj_score=f3(data_xj,'性价比')
#指标标准化得分

data_final_q1=pd.merge(data_kw_score,data_rj_score,left_index=True,right_index=True)
data_result=pd.merge(data_final_q1,data_xj_score,left_index=True,right_index=True)


'''
(3)绘制图表
'''
from bokeh.io import output_file 
from bokeh.plotting import figure,show 
output_file('餐饮图.html') 
from bokeh.models.annotations import Span 
from bokeh.models.annotations import BoxAnnotation 
from bokeh.layouts import gridplot 
from bokeh.models import ColumnDataSource


data_result['size'] = data_result['口味_norm']*40 
data_result.index.name = 'lb' 
data_result.columns = [['xjb','xjb_nor','kw','kw_nor','rj','rj_nor','size']] 
from bokeh.models import HoverTool 
source = ColumnDataSource(data = data_result) 
name = data_result.index.tolist() 
hover1 = HoverTool(tooltips=[("类别", "@lb"), 
                             ("人均消费", "@rj"), 
                             ("性价比得分", "@xjb_nor"), 
                             ("口味得分", "@kw_nor")])
    
p1 = figure(plot_width = 800 ,plot_height = 300,
            title = '餐饮类型得分情况',x_axis_label = '人均消费',
            y_axis_label = '性价比得分',
            tools=[hover1,'box_select,reset,xwheel_zoom,pan,crosshair'])
p1.circle('rj','xjb',source = source,size = 'size',
          line_dash = 'dashed',alpha=0.5,line_width = 1.5,line_color = 'black')
p1.ygrid.grid_line_dash = [4,6] 
p1.xgrid.grid_line_dash = [4,6] 
center = BoxAnnotation(left = 40,right = 80,fill_alpha = 0.1,fill_color = 'navy')
p1.add_layout(center) 
hover2 = HoverTool(tooltips=[("类别", "@lb"),
                             ("人均", "@rj"), 
                             ("性价比得分", "@xjb_nor"),
                             ("口味得分", "@kw_nor")]) 
p2 = figure(plot_width = 800 ,plot_height = 300,title = '口味得分',
             x_range = name,
             tools=[hover2,'box_select,reset,xwheel_zoom,pan,crosshair'])
p2.vbar(x = 'lb',bottom = 0, top = 'kw_nor',width =1,
         source = source,color = 'red',line_color = 'white') 
p2.ygrid.grid_line_dash = [4,6]  
p2.xgrid.grid_line_dash = [4,6] 
hover3 = HoverTool(tooltips=[("类别", "@lb"),
                              ("人均", "@rj"),
                              ("性价比得分", "@xjb_nor"), 
                              ("口味得分", "@kw_nor")])
p3 = figure(plot_width = 800 ,plot_height = 300,
                title = '人均消费得分',x_range = p2.x_range,
                tools=[hover3,'box_select,reset,xwheel_zoom,pan,crosshair']) 
p3.vbar(x = 'lb',bottom = 0, top = 'rj_nor',width =1,source = source,color = 'green',line_color = 'white') 
p3.ygrid.grid_line_dash = [4,6] 
p3.xgrid.grid_line_dash = [4,6] 
p = gridplot([p1],[p2],[p3]) 
show(p)

    

print('finished!')