#! /usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import hashlib
import requests
import hmac
import base64
import json

# -----------------------
bucket = ''
operator = ''
password= ''
# -----------------------

gmdate = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')#获取GMT时间
password_md5 = hashlib.md5(password.encode('utf-8')).hexdigest()#获取操作员密码的MD5值
string =  'POST' + '&' + '/pretreatment/' +  '&'  + gmdate #计算签名的string拼接
signature = hmac.new(password_md5,string,hashlib.sha1).digest().encode('base64').rstrip()#签名计算

#文件拉取的任务提交
tasks = [{
        'url' : 'http://pic55.nipic.com/file/20141208/19462408_171130083000_2.jpg',
        'random': False,
        'overwrite': True,
        'save_as':'/spider/spaiderman.jpg'
        }]

tasks_str = base64.b64encode(json.dumps(tasks))#任务json 然后base64

#content = requests.request(method = POST,api,data = data, headers = headers)
#提交请求
content = requests.post(
    url="http://p0.api.upyun.com/pretreatment/",
    headers={
        'Authorization': 'UPYUN ' + operator + ':' + signature,
        'Date': gmdate,
    },
    data={
            'service':bucket,
            'notify_url':'http://httpbin.org/post',
            'app_name':'spiderman',
            'tasks':tasks_str,
    },
)

print content.status_code
print content.text
print content.headers

if content.status_code == 200:
        print ('good job')
else:
        print ('fuck job')
