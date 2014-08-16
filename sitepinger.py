#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
from socket import gethostbyname
from sendemail import sendmsg
from datetime import datetime
import logging
import os
import time

import gevent
from gevent import monkey

os.environ['TZ'] = 'Europe/Amsterdam'
time.tzset()

workdir = '/home/username/sitepinger/'

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%d.%m.%Y %H:%M:%S',
                    filename= workdir + 'sitepinger.log',
                    filemode='a')

domains = [line.strip() for line in open(workdir + 'domains.txt')]

results = []

# number of attempts
# if script failed to ping website after Nattempts website is considered as
# 'Not responding'
Nattempts = 3

def responding(domain):
    for i in range(Nattempts):
        try:
            url = urllib2.urlopen('http://'+domain)
            http_code = url.getcode()
            if http_code == 200:
                print domain, 'OK'
                return True
        except Exception, e:
            pass
    print domain, 'ERR'
    error_sites.append(domain)
    logging.error(e)
    return False

def compose_msg(domains):
    time_now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    domains_list = '<br>'.join(map(lambda x:'<a href="http://{0}">{0}</a><br>'.format(x), domains))
    message = 'Time: {0}<br><br>{1}'.format(time_now, domains_list)
    return message

def compose_title(domains):
    domains_num = len(domains)
    if domains_num > 1:
        plural = 's are'
    else:
        plural = ' is'
    title = '{0} Domain{1} not responding'.format(domains_num, plural)
    return title

error_sites = []

logging.info('Check started ('+str(len(domains))+' domains)' )

jobs = [gevent.spawn(responding, domain) for domain in domains]

gevent.joinall(jobs) 

if len(error_sites) > 0:
    msg_title = compose_title(error_sites)
    msg_body = compose_msg(error_sites)
    sendmsg(msg_title, msg_body)
    logging.info(msg_title)    
    logging.info('Message has been sent')
else:
    logging.info('All websites are OK')    
