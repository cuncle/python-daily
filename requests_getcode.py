#! /usr/bin/env python
#coding=utf-8
import sys
import requests
def getHttpStatusCode(url):
    try:
        request = requests.get(url)
        httpStatusCode = request.status_code
        return httpStatusCode
    except requests.exceptions.HTTPError as e:
        return e

if __name__ == "__main__":
    with open('1.txt', 'r') as f:
        for line in f:
            try:
                status = getHttpStatusCode(line.strip('\n'))#换行符
                if status == 200:
                    with open('2.txt','a') as f:
                        f.write(line + '\n')
                        print line
                else:
                    print 'no 200 code'
            except Exception as e:
                print e
