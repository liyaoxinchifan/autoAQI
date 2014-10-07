#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import urllib2
import re
import smtplib
from email.mime.text import MIMEText

class Getpm:
    def pmnow(self, pmurl):
        fanhui = {}
        jieguo = urllib2.urlopen(pmurl)
        html = jieguo.read()
        riqire = re.compile(r'(?:<div style=\'font-weight:normal;font-size:9px;\'>)(.*?)</div>')
        pm25re = re.compile(r'(?:<td id=\'hdrpm25\'  align=center style=\'font-size:10px;\'>)(.*?)</td>')
        pm10re = re.compile(r'(?:<td id=\'hdrpm10\'  align=center style=\'font-size:10px;\'>)(.*?)</td>')
        fanhui['riqi'] = riqire.search(html).group(1)
        fanhui['pm25'] = pm25re.search(html).group(1)
        fanhui['pm10'] = pm10re.search(html).group(1)
        return fanhui

class Mypm25(Getpm):
    def __init__(self):
        self.maillist = ['example@example.com']
        self.mailsub = "AQI Today"
        self.mailhost = "smtp.qq.com"
        self.mailuser = "111111111"
        self.mailpass = "qqmailpassword"
        self.mailurl = "qq.com"
        self.smsuser = "smsusername"
        self.smspass = "smspassword"
        self.smsnu = "18500000000"
        self.smsurl = "http://www.smsbao.com/sms"

    def sendmail(self, content):
        me = "AQI" + "<" + self.mailuser + "@" + self.mailurl + ">"
        msg = MIMEText(content, _subtype='html', _charset='gb2312')
        msg['Subject'] = self.mailsub
        msg['From'] = me
        msg['To'] = ';'.join(self.maillist)
        try:
            s = smtplib.SMTP()
            s.connect(self.mailhost)
            s.login(self.mailuser, self.mailpass)
            s.sendmail(me, self.maillist, msg.as_string())
            s.close()
            return True
        except Exception, e:
            print str(e)
            return False

    def sendsms(self, content):
        mysms = {'u': self.smsuser, 'p': self.smspass, 'm': self.smsnu, 'c': content}
        try:
            requests.get(self.smsurl, params = mysms)
            return True
        except Exception:
            print 'Bad!!'
            return False

mypmurl = 'http://aqicn.info/?city=China/%E9%83%91%E5%B7%9E/%E7%BB%8F%E5%BC%80%E5%8C%BA%E7%AE%A1%E5%A7%94&widgetscript&size=large&id=5432408be050b9.87500165'
# mailpm = Mypm25()
smspm = Mypm25()
# fsnr = mailpm.pmnow(mypmurl)
fsnr = smspm.pmnow(mypmurl)
smscontent = '%s, PM2.5: %s, PM10: %s' % (fsnr['riqi'], fsnr['pm25'], fsnr['pm10'])
mailcontent = '''
<b>%s</b><p>
PM2.5:&nbsp;<b>%s</b><p>
PM10&nbsp;:&nbsp;<b>%s</b><p>
''' % (fsnr['riqi'], fsnr['pm25'], fsnr['pm10'])
# mailpm.sendmail(mailcontent)
smspm.sendsms(smscontent)