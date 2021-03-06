# Python
from urllib.parse import urlencode

# Packages
from django.conf import settings
from django.core.management import call_command
from django.test import Client, TestCase
from elasticsearch import Elasticsearch

# Project
from datasets.generic.tests.authorization import AuthorizationSetup
from datasets.generic.tests.authorization import AUTH_HEADER
from .factories import create_hr_data


class ESTestCase(TestCase):
    """
    TestCase for using with elastic search to reset the elastic index
    """

    @classmethod
    def rebuild_elastic_index(cls):
        """
        Rebuild the elastic search index for tests
        """
        es = Elasticsearch(hosts=settings.ELASTIC_SEARCH_HOSTS)

        call_command('elastic_indices', '--recreate', 'hr', verbosity=0)
        call_command('elastic_indices', '--build', 'hr', verbosity=0)

        es.cluster.health(wait_for_status='yellow',
                          wait_for_active_shards=0,
                          timeout="320s")


class DataselectieExportTest(ESTestCase, AuthorizationSetup):

    @classmethod
    def setUpTestData(cls):    # noqa
        super(ESTestCase, cls).setUpTestData()
        create_hr_data()
        cls.rebuild_elastic_index()

    def setUp(self):
        self.client = Client()
        self.setup_authorization()
        self.headers = {AUTH_HEADER: f'Bearer {self.token_default}'}

    def tearDown(self):
        pass

    def test_complete_export_hr(self):
        response = self.client.get('/dataselectie/hr/export/', **self.headers)
        self.assertEqual(response.status_code, 401)

        self.headers = {AUTH_HEADER: f'Bearer {self.token_scope_hr_r}'}
        response = self.client.get('/dataselectie/hr/export/', **self.headers)

        self.assertEqual(response.status_code, 200)

        res = (b''.join(response.streaming_content)).decode('utf-8').strip()
        res = res.split('\r\n')
        # 6 lines: headers + 5 items
        self.assertEqual(len(res), 7)
        # check columns length
        row2 = res[2].split(';')
        self.assertEqual(len(row2), 32)

    def test_export_hr_subcategorie(self):
        self.headers = {AUTH_HEADER: f'Bearer {self.token_scope_hr_r}'}
        q = {
            'page': 1,
            'subcategorie': 'groothandel (verkoop aan andere ondernemingen, niet zelf vervaardigd)'  # noqa
        }
        response = self.client.get(
            '/dataselectie/hr/export/?{}'.format(urlencode(q)), **self.headers)
        # assert that response status is 200
        self.assertEqual(response.status_code, 200)

        res = (b''.join(response.streaming_content)).decode('utf-8').strip()

        res = res.split('\r\n')
        # 2 lines: headers + 1 items
        self.assertEqual(len(res), 2)
