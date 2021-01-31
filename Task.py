#!/usr/bin/env python
# coding: utf-8

# # Action1：求2+4+6+8+...+100的求和，用Python该如何写?

#方法一
result=0
for i in range(2,102,2):
    result=result+i
print(result)
print(sum([i for i in range(2,102,2)]))#方法二
print(sum(range(2,102,2))) #方法三


# # Action2: 统计全班的成绩
# 班里有5名同学，现在需要你用Python来统计下这些人在语文、英语、数学中的平均成绩、最小成绩、最大成绩、方差、标准差。然后把这些人的总成绩排序，得出名次进行成绩输出（可以用numpy或pandas）

#Step1:建立数据表
from pandas import DataFrame
score = {'语文':[68, 95, 98, 90,80],  '数学':[65, 76, 86, 88, 90], '英语':[30, 98, 88, 77, 90]}
df= DataFrame(score, index=['张飞', '关羽', '刘备', '典韦', '许褚'], columns=['语文','数学', '英语'])

#Step2:各科的平均值、最大值他、最小值、方差、标准值
mean=df.mean()
max=df.max()
min=df.min()
std=df.std()
var=df.var()
result1=DataFrame(list(zip(mean,max,min,var,std)),index=["语文","数学","英语"],columns=["平均值","最大值","最小值","方差","标准差"])
print("A21各科的平均值、最大值他、最小值、方差、标准值\n",result1)

#Step3:求总分
sum_score=df.sum(axis=1)
#print("总分",sum_score)

#Step4:根据总分排名
sum_score=sum_score.sort_values(ascending=False)
print("A22总分排名\n",sum_score)

# # Action3: 对汽车质量数据进行统计

import pandas as pd
#Step1:数据加载
data=pd.read_csv('./car_complain.csv')

df_new=data.problem.str.get_dummies(',')
#df=df.drop('problem',axis=1)#0代表没有，1代表存在
data=data.drop('problem',axis=1).join(df_new)

#Step2:清洗数据
def f(x):
    x=x.replace('一汽-大众','一汽大众')
    return (x)
data['brand']=data['brand'].apply(f)

#A31:品牌投诉总数排序
result=data.groupby(['brand'])['id'].agg(['count'])
result=result.sort_values('count',ascending=False)
print("A31品牌投诉总数排序\n",result)


#A32:车型投诉总数排序
result2=data.groupby(['car_model'])['id'].agg(['count'])
result2=result2.sort_values('count',ascending=False)
print("A32车型投诉总数排序\n",result2)

#A33:哪个品牌的平均车型投诉最多
import numpy as np
result3=data.groupby(['brand','car_model'])['id'].agg(['count'])
#print(result3)
#01求品牌投诉总数
brand_complain_count=result3.groupby(['brand'])['count'].agg(['sum'])
#02求品牌对应的车型数
result5=result3.groupby(['brand','car_model']).agg(['count'])
brand_model_count=result5.groupby(['brand'])['count'].agg(['sum'])
#print(result4)
#print(result5)
#03求品牌的平均车型投诉数
avg_complain=DataFrame(np.divide(brand_complain_count,brand_model_count))
#04对品牌的平均车型投诉数排序
avg_complain=avg_complain.sort_values('sum',ascending=False)
avg_complain.rename(columns={'sum': 'average car complain'}, inplace = True)
print("A33各品牌的平均车型投诉排序\n",avg_complain)





