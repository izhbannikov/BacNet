# Scrapy settings for pubmed project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'pubmed'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['pubmed.spiders']
NEWSPIDER_MODULE = 'pubmed.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
URLLENGTH_LIMIT = 25000

