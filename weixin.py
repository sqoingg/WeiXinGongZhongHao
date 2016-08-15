# -*- coding: utf-8 -*-
import hashlib
import web
import lxml
import time
import os
import urllib2,json
from lxml import etree

urls = (
'/.*','WeixinInterface'
)
app=web.application(urls,globals())

class WeixinInterface:

    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        #��ȡ�������
        data = web.input()
        signature=data.signature
        timestamp=data.timestamp
        nonce=data.nonce
        echostr=data.echostr
        #�Լ���token
        token="weixin" #�����д����΢�Ź���ƽ̨�������token
        #�ֵ�������
        list=[token,timestamp,nonce]
        list.sort()
        sha1=hashlib.sha1()
        map(sha1.update,list)
        hashcode=sha1.hexdigest()
        #sha1�����㷨        

        #���������΢�ŵ�������ظ�echostr
        if hashcode == signature:
            return echostr
    def POST(self):        
        str_xml = web.data() #���post��������
        xml = etree.fromstring(str_xml)#����XML����
        content=xml.find("Content").text#����û������������
        msgType=xml.find("MsgType").text
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text
        def youdao(word):
            qword = urllib2.quote(word)
            baseurl = r'http://fanyi.youdao.com/openapi.do?keyfrom=fanyii&key=1281815706&type=data&doctype=json&version=1.1&q='
            url = baseurl+qword
            resp = urllib2.urlopen(url)
            fanyi = json.loads(resp.read())
            ##����json�Ƿ񷵻�һ���С�basic����key���ж��Ƿ���ɹ�
            if 'basic' in fanyi.keys():
                ##����������������֯��ʽ
                trans = u'%s:\n%s\n%s\n�������壺\n%s'%(fanyi['query'],''.join(fanyi['translation']),''.join(fanyi['basic']['explains']),''.join(fanyi['web'][0]['value']))
                return trans
            else:
                return u'�Բ���������ĵ���%s�޷����룬����ƴд'% word
        Nword = youdao(content)        
        return self.render.reply_text(fromUser,toUser,int(time.time()),Nword)

if __name__=="__main__":
	web.wsgi.runwsgi=lambda func, addr=None:web.wsgi.runfcgi(func,addr)
	app.run()