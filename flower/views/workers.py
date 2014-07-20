from __future__ import absolute_import

import json

from tornado import web
from tornado import gen
from tornado.httpclient import AsyncHTTPClient

from ..views import BaseHandler


class WorkerView(BaseHandler):
    @web.authenticated
    @gen.coroutine
    def get(self, name):
        refresh = self.get_argument('refresh', default=False, type=bool)

        url = self.request.protocol + "://" + self.request.host + "/api/workers"
        url += "?workername=%s" % name
        if refresh:
            url += '&refresh=%s' % refresh

        http_client = AsyncHTTPClient()
        try:
            response = yield http_client.fetch(url)
            worker = json.loads(response.body)[name]
        except AttributeError:
            raise web.HTTPError(404, "Unknown worker '%s'" % name)
        finally:
            http_client.close()

        worker['name'] = name
        self.render("worker.html", worker=worker)
