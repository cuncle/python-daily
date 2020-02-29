# /usr/env/bin python
# -*- coding: utf-8 -*-#

import requests
import json
import time
import re
import unicodedata

'''
获取access token 
'''
def get_access_token(appId,appSecret):
    tokenUrl="https://api.weixin.qq.com/cgi-bin/token"
    querystring = {"grant_type": "client_credential",
                   "appid": appId,
                   "secret": appSecret
                   }
    headers = {
        'cache-control': "no-cache"
    }
    response = requests.request("GET", url=tokenUrl, headers=headers, params=querystring)
    #print(response.json()['access_token'])
    access_token= response.json()['access_token']
    return access_token

'''
获取数据库需要查询的次数，max_limt and batchtimes
'''
def get_database_max(access_token):
    databaseurl = 'https://api.weixin.qq.com/tcb/databasequery'
    queryString = {'access_token': access_token}
    payload = {"env": "shenzhen-xmeqf",
               "query": "db.collection(\'messages\').count()"
               }
    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache"
    }
    response = requests.request("POST", url=databaseurl, data=json.dumps(payload), headers=headers, params=queryString)
    max_limt=(response.json()['pager']['Total'])#计算一共读取的次数
    batchTimes=max_limt//10 #计算需分几次取
    return batchTimes

'''
查询数据
'''

def get_database(access_token,template_id,city,query):
    try:
        databaseurl='https://api.weixin.qq.com/tcb/databasequery'
        queryString={'access_token':access_token}
        payload={"env":"shenzhen-xmeqf",
             "query":query
             }
        headers = {
        'content-type': "application/json",
        'cache-control': "no-cache"
        }
        response=requests.request("POST",url=databaseurl,data=json.dumps(payload),headers=headers,params=queryString)
        for i in range(len(response.json()['data'])):
            all_json=json.loads(response.json()['data'][i])
            touser=all_json['touser']
            data_uname=all_json['uname']
            yaohaodata=yaohao(data_uname,city) #查询摇号结果信息
            if((yaohaodata is None) and (is_number(data_uname) is True) ):
                result="未中签"
                tid=data_uname #摇号编号
                uname="空"#摇号姓名
                eid=time.strftime("%Y年第%m期")#摇号期数
                unote="申请编号3个月有效，请登录官网延长有效期"
                send_message(access_token, touser, template_id, result, tid, eid,uname,unote)
            elif(yaohaodata is None ):
                result="未中签"
                tid=0 #摇号编号
                uname=data_uname#摇号姓名
                #eid="2020年第1期"
                eid=time.strftime("%Y年第%m期")#摇号期数
                unote="申请编号3个月有效，请登录官网延长有效期"
                send_message(access_token, touser, template_id, result, tid, eid,uname,unote)
            else:
                #发送模板消息_
                tid=yaohaodata[0]
                uname=yaohaodata[1]
                eid=yaohaodata[2]
                result='中签'
                unote = "同名中签结果只显示最新,建议核对一下编号"
                send_message(access_token, touser, template_id, result, tid, eid,uname,unote)

    except Exception as err:
        print('Other error: {}'.format(err))
    pass

'''
查询摇号结果
'''
def yaohao(uname,city):
    try:
        baiduurl='https://sp0.baidu.com/9_Q4sjW91Qh3otqbppnN2DJv/pae/common/api/yaohao'
        baiducb = 'jQuery110201476696_'
        queryString = {'name': uname,
                   'city':city,
                   'format':'json',
                   'resource_id':'40003',
                   'cb':baiducb,
                   '_': time.time()}
        headers ={
        'content-type': 'text/html; charset=UTF-8;',
        'Host': 'sp0.baidu.com',
        'Referer': 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=%E6%B7%B1%E5%9C%B3%E6%91%87%E5%8F%B7&rsv_pq=e6982f520002bd9f&rsv_t=8a99s%2BuxJCLrxlWzPUAxoSV1XjHD8jlrLpkhZmwKEjfFZzhD8HfqC5IoL9o&rqlang=cn&rsv_enter=1&rsv_sug3=22&rsv_sug1=30&rsv_sug7=101&rsv_sug2=0&inputT=4991&rsv_sug4=5251',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
        'Accept': '*/*'
             }
        response = requests.request("GET",url=baiduurl,params=queryString)
        print(response.text)
        m = re.search('{.*\}', response.text)
        if(json.loads(m.group(0))['data'][0]['dispNum']!="0"):
            yaohao_result=json.loads(m.group(0))['data'][0]['disp_data'][-1]#摇中的最后一个结果
            result_tid=yaohao_result['tid']#摇中编号
            result_name=yaohao_result['name']#摇中的姓名
            result_eid = yaohao_result['eid']#摇中的期数
            return result_tid,result_name,result_eid
        else:
            return None
            #print('没有摇中')
    #程序的异常处理
    except KeyError as err:
        print('KeyError: {}'.format(err))
    except Exception as err:
        print('Other error: {}'.format(err))
    pass

'''
发送订阅消息
'''
def send_message(access_token,touser,template_id,result,tid,eid,uname,unote):
    try:
        url = "https://api.weixin.qq.com/cgi-bin/message/subscribe/send"
        querystring = {
        "access_token": access_token}
        payload={
            "touser": touser,
            "template_id": template_id,
            "page": "pages/index/index",
            "data": {
                    "phrase1": {
                                 "value": result
                                },
                    "character_string2": {
                                "value": tid
                                },
                    "thing3": {
                                "value": eid
                            },
                    "name4":{
                            "value":uname
                    },
                    "thing5":{
                        "value":unote
                    }
                    }
            }
        headers = {
        'content-type': "application/json"
        }
        response = requests.request("POST", url, data=json.dumps(payload), headers=headers, params=querystring)
    except KeyError as err:
        print('KeyError: {}'.format(err))
    except Exception as err:
        print('Other error: {}'.format(err))
    pass

'''
判断是否为数字
'''
def is_number(s):
    try:
        float(s)
        return True
    except ValueError as err:
        print('ValueError: {}'.format(err))
        pass
    try:
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError) as err:
        print('Error: {}'.format(err))
        pass
    return False


if __name__ == '__main__':
    appId=''#小程序的appid
    appSecret=''#小程序的appSecret
    template_id='' #订阅消息的模板id
    city = ''  # 配置查询结果城市
    Max_limt = 10 #单次获取数据量
    access_token=get_access_token(appId,appSecret)
    batchTimes=get_database_max(access_token)
    if(int(batchTimes)==0):
        query="db.collection(\'messages\').field({touser: true,uname:true}).orderBy('touser', 'desc').skip(0).limit(10).get()"
        get_database(access_token, template_id, city, query)
    else:
        i=1
        for i in range(1, (batchTimes+2)):
            query="db.collection(\'messages\').field({touser: true,uname:true}).orderBy(\'touser\', \'desc\').skip(" + str(i*Max_limt) +").limit(" + str(Max_limt) +").get()"
            print(query)
            i=i+1
            get_database(access_token, template_id, city, query)
