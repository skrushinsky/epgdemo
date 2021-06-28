import os
import sys
import unittest
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '..')) 
from api import app


VALID_EVENT = {
  "jobid": "sdf4-dsfssd-sdfs-43fsdf",
  "id_provider": 1011,
  "id_channel": 2882,
  "week": "19-04-2022",
  "href": "https://storage.yandexcloud.net/epgparserasync/1012/2882/2021-04-12.json",
  "spider_name": "tt_ru"
}

INVALID_EVENT = {
  "jobid": "sdf4-dsfssd-sdfs-43fsdf",
  "id_provider": 'foo',
  "id_channel": 2882,
  "week": "19-04-2022",
  "href": "https://storage.yandexcloud.net/epgparserasync/1012/2882/2021-04-12.json",
  "spider_name": "tt_ru"
}

class BasicTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        # self.assertEqual(app.debug, False)
 
 
    def test_root(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_valid_post(self):
        resp = self.app.post('/service/hook', 
                             data=json.dumps(VALID_EVENT), 
                             content_type='application/json')
        self.assertEqual(resp.status_code, 201)

    def test_invalid_post(self):
        resp = self.app.post('/service/hook', 
                             data=json.dumps(INVALID_EVENT), 
                             content_type='application/json')

        self.assertEqual(resp.status_code, 400)

    def test_404(self):
        resp = self.app.get('/foo')
        self.assertEqual(resp.status_code, 404)


if __name__ == "__main__":
    unittest.main()