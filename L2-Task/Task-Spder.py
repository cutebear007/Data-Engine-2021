#time:2021/2/6
#Author:ZhangJian
"""Task:Action1：汽车投诉信息采集：数据源：http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-1.shtml
投诉编号，投诉品牌，投诉车系，投诉车型，问题简述，典型问题，投诉时间，投诉状态,可以采用Python爬虫，或者第三方可视化工具"""

import requests
from bs4 import BeautifulSoup
import pandas as pd


#下载器函数
def get_page_content(url):
    # 得到页面的内容
    #Headers是解决requests请求反爬的方法之一
    headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    html=requests.get(url,headers=headers,timeout=10)
    content = html.text
    #print(content)
    # 通过content创建BeautifulSoup对象
    soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
    return soup

#解析内容函数
def analysis(soup):
    df=pd.DataFrame(columns=[ 'id','brand','car_model','type','desc','problem','datetime','status'])
    temp=soup.find('div',class_='tslb_b')
    tr_list=temp.find_all("tr")
    for tr in tr_list:
        td_list=tr.find_all("td")
        #如果没有td，就是表头，th
        if len(td_list)>0:
            id,brand,car_model,type,desc,problem,datetime,status=td_list[0].text,td_list[1].text,\
                                                                 td_list[2].text,td_list[3].text,td_list[4].text,\
                                                                 td_list[5].text, td_list[6].text, td_list[7].text
            temp={}
            temp['id']=id
            temp['brand'] =brand
            temp['car_model'] =car_model
            temp['type'] = type
            temp['desc'] =desc
            temp['problem'] = problem
            temp['datetime'] =datetime
            temp['status'] = status
            df=df.append(temp,ignore_index=True)
    return df

content=pd.DataFrame(columns=['id', 'brand', 'car_model', 'type', 'desc', 'problem', 'datetime', 'status'])
#主函数，翻页循环
for page_num in range(1,11,1):#作为示例，爬取10页的内容
    url='http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-0-0-0-0-0-'+str(page_num)+'.shtml'
    soup = get_page_content(url)
    print("已完成第%d页解析"%(page_num))
    df = analysis(soup)
    #print(df)
    content=content.append(df,ignore_index=True)
#表格的列明重命名
content.rename(columns={'id': '投诉编号', 'brand': '投诉品牌','car_model':'投诉车系',\
                        'type': '投诉车型', 'desc': '问题描述','problem':'典型问题',\
                        'datetime': '投诉时间', 'status': '投诉状态'},inplace = True)
#输出与保存爬取结果
print('前%d页爬取内容\n'%(page_num),content)
content.to_excel('车质网信息2010-2021.xlsx',index=False)



