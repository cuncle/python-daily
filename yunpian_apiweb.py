# /usr/env/bin python
# -*- coding: utf-8 -*-#
import requests
def upload_file(path, filename, wksid, token, subAccountId, isDuplicateCheck=True):
    upload_url='https://www.yunpian.com/api/manual/file/upload'
    try:
        cookies = {
            '__wksid': wksid,
        }
        headers = {
            'Yp-Acctok-Request': token
         }
        data = {
            'subAccountId': subAccountId,
            'activityId': None,
            'isDuplicateCheck': isDuplicateCheck,
            'type': 0
        }
        pwd = path + filename
        files = {'phonesFile': open(pwd, 'rb')}
        response = requests.post(url=upload_url,data=data,cookies=cookies,headers=headers,files=files)
        return response.json()['data']['activityId']
    except requests.exceptions.RequestException:
            print('HTTP Request failed')
    except Exception as err:
        print('Other error: {}'.format(err))

def send(activityId, wksid, token, content, subAccountId, signature, phones,
         isDuplicateCheck=True, isFilterDayDuplicate=False, isFromFile=True,
         isScheduled=False, mobileStat=True, notifyType=0, scheduleTime=None):
    send_url='https://www.yunpian.com/api/domestic/sms/broadcast/put'
    try:
        cookies = {
            '__wksid': wksid,
        }
        headers = {
            'Yp-Acctok-Request': token
        }
        data = {
        'activityId': activityId,
        'content': content,
        'isDuplicateCheck': isDuplicateCheck,
        'isFilterDayDuplicate': isFilterDayDuplicate,
        'isFromFile': isFromFile,
        'isScheduled': isScheduled,
        'mobileStat': mobileStat,
        'notifyType': notifyType,
        'phones': phones,
        'scheduleTime': scheduleTime,
        'signature': signature,
        'subAccountId': subAccountId
        }
        response = requests.post(url=send_url,headers=headers,cookies=cookies,json=data)
        print(response.text)
    except requests.exceptions.RequestException:
        print('HTTP Request failed')
    except Exception as err:
        print('Other error: {}'.format(err))
    pass



if __name__ == '__main__':
    path = '/Users/cxiang/Downloads/cxiang01/'
    list_filename_and_content = [
        ["111.xlsx", "测试通知2"],
        ["222.xlsx", "测试通知3"]
    ]
    wksid = 'n-9D18F71F013545FD8A6A1C73CF408707'#cookies中的wksid
    token = '99NXy4vbx9XIwEcRLkTbsdMnK7PH+g4Obtq3XwG3AlfW+svvH/+dgPRVVVasK+mxZTjxBJnDY/w='#yp-access-token
    sub_id = '890000000020461940'#云片子号
    signature = '【云片网】'#签名
    for i in range(len(list_filename_and_content)):
        filename=list_filename_and_content[i][0]
        content = list_filename_and_content[i][1]
        activityId = upload_file(path, filename, wksid, token, sub_id)
        send(activityId, wksid, token, content, sub_id, signature, [])
