#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import urllib.error
import re
import ssl
import io
import gzip
import random
import socket
import time
import area

socket.setdefaulttimeout(5.0)


class Tools(object):

    def __init__(self):
        pass

    def getPage(self, url, requestHeader=[], postData={}):
        fakeIp = self.fakeIp()
        requestHeader.append('CLIENT-IP:' + fakeIp)
        requestHeader.append('X-FORWARDED-FOR:' + fakeIp)

        if postData == {}:
            request = urllib.request.Request(url)
        elif isinstance(postData, str):
            request = urllib.request.Request(url, postData)
        else:
            request = urllib.request.Request(url, urllib.parse.urlencode(postData).encode('utf-8'))

        for x in requestHeader:
            headerType = x.split(':')[0]
            headerCon = x.replace(headerType + ':', '')
            request.add_header(headerType, headerCon)

        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            response = urllib.request.urlopen(request, context=ctx)
            header = response.headers
            body = response.read().decode('utf-8')
            code = response.code
        except urllib.error.HTTPError as e:
            header = e.headers
            body = e.read().decode('utf-8')
            code = e.code

        result = {
            'code': code,
            'header': header,
            'body': body
        }

        return result

    def fakeIp(self):
        fakeIpList = []

        for x in range(0, 4):
            fakeIpList.append(str(int(random.uniform(0, 255))))

        fakeIp = '.'.join(fakeIpList)

        return fakeIp

    def fmtCookie(self, string):
        result = re.sub(r"path\=\/.", "", string)
        result = re.sub(r"(\S*?)\=deleted.", "", result)
        result = re.sub(r"expires\=(.*?)GMT;", "", result)
        result = re.sub(r"domain\=(.*?)tv.", "", result)
        result = re.sub(r"httponly", "", result)
        result = re.sub(r"\s", "", result)

        return result

    def urlencode(self, str):
        reprStr = repr(str).replace(r'\x', '%')
        return reprStr[1:-1]

    def gzdecode(self, data):
        try:
            compressedstream = io.StringIO(data)
            gziper = gzip.GzipFile(fileobj=compressedstream)
            html = gziper.read()
            return html
        except:
            return data

    def fmtTitle(self, string):
        pattern = re.compile(r"(cctv[-|\s]*\d*)?(.*)", re.I)
        tmp = pattern.findall(string)
        channelId = tmp[0][0].strip('-').strip()
        channel_title = tmp[0][1]

        channel_title = channel_title.replace('.m3u8', '')

        pattern = re.compile(r"<.*?>", re.I)
        channel_title = re.sub(pattern, "", channel_title)

        pattern = re.compile(r"(FHD|HD|SD|4K|高清|全高清)", re.I)
        tmp = pattern.findall(channel_title)
        quality = ''
        if len(tmp) > 0:
            quality = tmp[0]
            channel_title = channel_title.replace(tmp[0], '')

        result = {
            'id': channelId,
            'title': channel_title.strip('-').strip(),
            'quality': quality.strip('-').strip().upper(),
            'level': 4,
        }

        if result['id'] != '':
            pattern = re.compile(r"cctv[-|\s]*(\d*)", re.I)
            result['id'] = re.sub(pattern, "CCTV-\\1", result['id'])

            if '+' in result['title']:
                result['id'] = result['id'] + str('+')

        pattern = re.compile(r"\[\d+\*\d+\]", re.I)
        result['title'] = re.sub(pattern, "", result['title'])

        Area = area.Area()
        result['level'] = Area.classify(str(result['id']) + str(result['title']))

        # Radio
        pattern = re.compile(r"(radio|fm)", re.I)
        tmp = pattern.findall(result['title'])
        if len(tmp) > 0:
            result['level'] = 7

        return result

    def chkPlayable(self, url):
        try:
            startTime = int(round(time.time() * 1000))
            code = urllib.request.urlopen(url).getcode()
            if code == 200:
                endTime = int(round(time.time() * 1000))
                useTime = endTime - startTime
                return int(useTime)
            else:
                return 0
        except:
            return 0

    def chkCros(self, url):
        return 0
        # try:
        #     res = urllib.request.urlopen(url).getheader('Access-Control-Allow-Origin')

        #     if res == '*' :
        #         return True
        #     else :
        #         return False
        # except:
        #     return 0
