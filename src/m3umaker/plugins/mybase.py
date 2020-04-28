#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tools
import time
import re


class Source(object):

    def __init__(self):
        self.T = tools.Tools()
        self.now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def getSource(self):
        urlList = []
        sourcePath = './plugins/mybase_source'
        sourcePath = '/Users/dwei/Workspace/IdeaProjects/live/doc/bak/tv.m3u'
        fo = open(sourcePath, "r+")

        tmp = fo.read();
        pattern = re.compile(r"#EXTINF:-1(.*?)\n(.*?)\n", re.I | re.S)
        sourceList = pattern.findall(tmp)

        i = 1
        total = len(sourceList)
        for item in sourceList:
            info = self.T.fmtTitle(item[0].strip().replace(',', '', 1))
            print('Checking[ %3s / %3s ]: %-8s' % (i, total, str(info['id']) + str(info['title']).split(',')[-1]), end="\t")
            i = i + 1

            # netstat = 0
            # for k in range(5):
            #     netstat = self.T.chkPlayable(item[1])
            #     print('try checking \033[32m%s\033[0m次，time%s' % (k,netstat))
            #     if(netstat>0):
            #         break

            netstat = self.T.chkPlayable(item[1])
            if netstat > 0:
                print('\033[32m%5sms\033[0m' % netstat)
                cros = 1 if self.T.chkCros(item[1]) else 0
                data = {
                    'title': str(info['id']) if info['id'] != '' else str(info['title']).split(',')[-1],
                    'url': str(item[1]),
                    'quality': str(info['quality']),
                    'delay': netstat,
                    'level': str(info['level']),
                    'cros': cros,
                    'online': 1,
                    'udTime': self.now,
                    'extInf': str(info['id']) if info['id'] != '' else str(info['title'])
                }
                urlList.append(data)
            else:
                print('\033[31m%5sms\033[0m' % netstat)
                pass  # MAYBE later :P

        return urlList
