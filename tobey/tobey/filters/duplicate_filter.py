import os
import sqlite3

from scrapy.dupefilter import BaseDupeFilter #RFPDupeFilter
from scrapy.utils.request import request_fingerprint
from scrapy.utils.job import job_dir
from scrapy.conf import settings

class SqliteDupeFilter(BaseDupeFilter):

    def __init__(self, path):
        if path is None:
            path = settings.get('SQLITE_PATH', "/tmp")
        filename = os.path.join(path, 'dupefilter.sqlite')
        self.conn = sqlite3.connect(filename, check_same_thread=False)
        q = """
            CREATE TABLE IF NOT EXISTS crawl_history(
                fp text primary key,
                link text
            )
            """
        self.conn.execute(q)
        self.conn.commit()

    def request_seen(self, request):
        fp = request_fingerprint(request)
        q = 'INSERT INTO crawl_history VALUES (?, ?)'
        args = (fp, request.url)
        try:
            self.conn.execute(q, args)
            self.conn.commit()
        except sqlite3.IntegrityError:
            return True

    @classmethod
    def from_settings(cls, settings):
        return cls(job_dir(settings))
