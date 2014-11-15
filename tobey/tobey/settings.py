# -*- coding: utf-8 -*-

# Scrapy settings for appnz project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
DEBUG = True
BOT_NAME = 'tobey'

SPIDER_MODULES = ['tobey.spiders']
NEWSPIDER_MODULE = 'tobey.spiders'

ITEM_PIPELINES = ['tobey.pipelines.AppnzPipeline', 'tobey.pipelines.WordPressXMLRPCPipeline']

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"

# LOG
#Minimum level to log. Available levels are: CRITICAL, ERROR, WARNING, INFO, DEBUG.
LOG_FILE = '/tmp/scrapy.log'
LOG_LEVEL = 'INFO'
LOG_ENABLED = True
LOG_STDOUT = True

DUPEFILTER_CLASS = 'tobey.filters.duplicate_filter.SqliteDupeFilter'


import logging
from scrapy import log
logfile = open('/tmp/observer.log', 'w+')
observer = log.ScrapyFileLogObserver(logfile, level=logging.INFO)
observer.start()

#SQLITE_PATH='/Users/zhanghui/github/startup/spider.appcheckin.com/'
SQLITE_PATH='/tmp/'
WP_USER = "admin"
WP_PASSWORD = "password"
WP_URL = "http://www.fx-dev.com/xmlrpc.php"
WP_BLOGID = ""
WP_TRANSPORT = ""
GOTO_SOURCE = u'<p><a href="%s" title="良心跳转" target="_blank">[查看原文]</a></p>'


