# -*- coding=utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import sys
import datetime
import xmlrpclib
import urllib
from scrapy.conf import settings
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import posts, media


class WordPressXMLRPCPipeline(object):

    def __init__(self):
        self.client = Client(settings.get('WP_URL'),
                             settings.get('WP_USER'),
                             settings.get('WP_PASSWORD'),
                             settings.get('WP_BLOGID'))

    def create_thumbnail(self, item):
        src = item['thumbnail_src'].encode('utf-8')
        img_name = 'wp-' + src.split('/')[-1]
        img_save_to = os.path.join('/tmp', img_name)
        remote_img = urllib.urlopen(src)
        with open(img_save_to, 'wb') as output:
            output.write(remote_img.read())

        data = {
            'name': img_name,
            'type': 'image/jpeg',
        }
        with open(img_save_to, 'rb') as img_file:
            data['bits'] = xmlrpc_client.Binary(img_file.read())

        response = self.client.call(media.UploadFile(data))
        try:
            os.remove(img_save_to)
        except:
            pass
        return response['id']

    def process_item(self, item, spider):
        post = WordPressPost()
        post.title = item['title']
        post.content = item['content'] + settings.get('GOTO_SOURCE', "[%s]") % item['link']
        post.date = datetime.datetime.strptime(item['publish_date'],
                                            "%Y-%m-%d %H:%M")
        post.terms_names = {
            'post_tag': item['tag'],
            'category': item['category'] if len(item['category']) > 0 else ['gist'],
        }
        post.post_status = 'publish'
        post.thumbnail = self.create_thumbnail(item)
        post.id = self.client.call(posts.NewPost(post))
        return item


class AppnzPipeline(object):
    def process_item(self, item, spider):
        return item
