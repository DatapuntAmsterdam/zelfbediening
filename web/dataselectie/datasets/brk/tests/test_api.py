import json
import logging
# Python
from urllib.parse import urlencode

# Packages
from django.conf import settings
from django.contrib.gis.geos import Polygon
from django.core.management import call_command
from django.test import Client, TestCase, tag, TransactionTestCase
from elasticsearch import Elasticsearch

from datasets.bag.tests import fixture_utils as bag
from datasets.brk.filters import modify_queryparams_for_shape
from datasets.brk.tests import fixture_utils as brk
from datasets.brk.tests.factories import create_brk_data
# Project
from datasets.generic.tests.authorization import AuthorizationSetup

BRK_BASE_QUERY = '/dataselectie/brk/?{}'
BRK_GEO_QUERY = '/dataselectie/brk/geolocation/?{}'
BRK_KOT_QUERY = '/dataselectie/brk/kot/?{}'
BRK_EXPORT_QUERY = '/dataselectie/brk/export/?{}'

log = logging.getLogger(__name__)


class ESTestCase(TransactionTestCase):
    """
    TestCase for using with elastic search to reset the elastic index
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.setUpTestData()

    @classmethod
    def setUpTestData(cls):
        """Load initial data for the TestCase."""
        pass

    @classmethod
    def rebuild_elastic_index(cls):
        """
        Rebuild the elastic search index for tests
        """
        es = Elasticsearch(hosts=settings.ELASTIC_SEARCH_HOSTS)

        call_command('elastic_indices', '--recreate', 'brk', verbosity=0)
        call_command('elastic_indices', '--build', 'brk', verbosity=0)

        es.cluster.health(
            wait_for_status='yellow',
            wait_for_active_shards=0,
            timeout="320s")


class DataselectieApiTest(ESTestCase, AuthorizationSetup):

    @classmethod
    def setUpTestData(cls):
        # super(ESTestCase, cls).setUpTestData()

        bag.create_gemeente_fixture()
        bag.create_buurt_combinaties()
        bag.create_buurt_fixtures()
        bag.create_gebiedsgericht_werken_fixtures()
        bag.create_stadsdeel_fixtures()

        create_brk_data()
        eigendom = brk.create_eigendom()[0][0]
        cls.kot = eigendom.kadastraal_object
        log.info( cls.kot.stadsdelen.all())

        brk.create_geo_tables()
        cls.rebuild_elastic_index()

    def setUp(self):
        brk.create_geo_data(self.kot)

        self.client = Client()
        self.setup_authorization()

    def test_get_geodata_withzoom_withoutbbox(self):
        # no zoom should work, takes default
        q = {'eigenaar_cat': 'Amsterdam'}
        response = self.client.get(BRK_GEO_QUERY.format(urlencode(q)),
                                   **self.header_auth_scope_brk_plus)
        self.assertEqual(response.status_code, 200)

        # zoom < 13 should work
        q['zoom'] = 12
        response = self.client.get(BRK_GEO_QUERY.format(urlencode(q)),
                                   **self.header_auth_scope_brk_plus)
        self.assertEqual(response.status_code, 200)

        # zoom >= 13 requires bbox
        q['zoom'] = 13
        response = self.client.get(BRK_GEO_QUERY.format(urlencode(q)),
                                   **self.header_auth_scope_brk_plus)
        self.assertEqual(response.status_code, 400)

    def test_get_geodata_with_bbox(self):
        q = {'eigenaar_cat': 'Amsterdam', 'zoom': 14}
        q['bbox'] = brk.get_bbox_leaflet()
        response = self.client.get(BRK_GEO_QUERY.format(urlencode(q)),
                                   **self.header_auth_scope_brk_plus)
        self.assertEqual(response.status_code, 200)

    def test_get_geodata_appartementen(self):
        q = {'eigenaar_cat': 'De staat', 'zoom': 12, 'bbox': brk.get_bbox_leaflet()}
        response = self.client.get(BRK_GEO_QUERY.format(urlencode(q)),
                                   **self.header_auth_scope_brk_plus)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['appartementen']), 0)
        q['zoom'] = 13
        response = self.client.get(BRK_GEO_QUERY.format(urlencode(q)),
                                   **self.header_auth_scope_brk_plus)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['appartementen']), 1)

    @tag('geo')
    def test_get_geodata_eigenpercelen(self):
        q = {'eigenaar_cat': 'De staat', 'bbox': brk.get_bbox_leaflet()}

        for zoom in range(8, 14):
            q['zoom'] = zoom
            response = self.client.get(BRK_GEO_QUERY.format(urlencode(q)),
                                       **self.header_auth_scope_brk_plus)
            self.assertEqual(response.status_code, 200)
            self.assertGeoJSON(response.json()['eigenpercelen'])

    @tag('geo')
    def test_get_geodata_nieteigenpercelen(self):
        q = {'eigenaar_cat': 'De staat', 'bbox': brk.get_bbox_leaflet()}

        for zoom in range(8, 14):
            q['zoom'] = zoom
            response = self.client.get(BRK_GEO_QUERY.format(urlencode(q)),
                                       **self.header_auth_scope_brk_plus)
            self.assertEqual(response.status_code, 200)
            self.assertGeoJSON(response.json()['niet_eigenpercelen'])

    @tag('geo')
    def test_get_geodata_gebied_buurt(self):
        q = {'eigenaar_cat': 'De staat', 'zoom': 14, 'bbox': brk.get_bbox_leaflet(), 'buurt_naam': 'Stationsplein e.o.'}
        response = self.client.get(BRK_GEO_QUERY.format(urlencode(q)),
                                   **self.header_auth_scope_brk_plus)
        self.assertValidEmpty(response)

        q['buurt_naam'] = 'BG-terrein e.o.'
        response = self.client.get(BRK_GEO_QUERY.format(urlencode(q)),
                                   **self.header_auth_scope_brk_plus)
        self.assertValidMatching(response, zoomed_in=True)

        q['zoom'] = 11
        response = self.client.get(BRK_GEO_QUERY.format(urlencode(q)),
                                   **self.header_auth_scope_brk_plus)
        self.assertValidMatching(response)

        q['buurt_naam'] = 'Stationsplein e.o.'
        response = self.client.get(BRK_GEO_QUERY.format(urlencode(q)),
                                   **self.header_auth_scope_brk_plus)
        self.assertValidEmpty(response)

    def test_get_geodata_eigenaar(self):
        q = {'zoom': 11, 'bbox': brk.get_bbox_leaflet(),
             'eigenaar_type': 'Pandeigenaar', 'eigenaar_cat': 'De staat'}
        response = self.client.get(BRK_GEO_QUERY.format(urlencode(q)),
                                   **self.header_auth_scope_brk_plus)
        self.assertValidEmpty(response)
        q['eigenaar_type'] = 'Appartementseigenaar'
        response = self.client.get(BRK_GEO_QUERY.format(urlencode(q)),
                                   **self.header_auth_scope_brk_plus)
        self.assertValidMatching(response, appartementen=True)

        q['zoom'] = 14
        response = self.client.get(BRK_GEO_QUERY.format(urlencode(q)),
                                   **self.header_auth_scope_brk_plus)
        self.assertValidMatching(response, zoomed_in=True, appartementen=True)

        q['eigenaar_type'] = 'Pandeigenaar'
        response = self.client.get(BRK_GEO_QUERY.format(urlencode(q)),
                                   **self.header_auth_scope_brk_plus)
        self.assertValidEmpty(response)

    def test_get_geodata_appartement_geen_eigenaar_cat(self):
        q = {'zoom': 14, 'bbox': brk.get_bbox_leaflet(),
             'eigenaar_type': 'Appartementseigenaar'}
        response = self.client.get(BRK_GEO_QUERY.format(urlencode(q)),
                                   **self.header_auth_scope_brk_plus)
        self.assertValidMatching(response, zoomed_in=True, appartementen=True)

        q['zoom'] = 11
        response = self.client.get(BRK_GEO_QUERY.format(urlencode(q)),
                                   **self.header_auth_scope_brk_plus)
        self.assertValidMatching(response, appartementen=True)

    def test_get_geodata_with_shape(self):
        q = {'eigenaar_cat': 'De staat', 'zoom': 14, 'bbox': brk.get_bbox_leaflet(),
             'buurt_naam': 'Stationsplein e.o.', 'shape': brk.get_selection_shape()}
        response = self.client.get(BRK_GEO_QUERY.format(urlencode(q)),
                                   **self.header_auth_scope_brk_plus)
        self.assertValidEmpty(response)

        q['buurt_naam'] = 'BG-terrein e.o.'
        response = self.client.get(BRK_GEO_QUERY.format(urlencode(q)),
                                   **self.header_auth_scope_brk_plus)
        self.assertValidMatching(response, zoomed_in=True)

        q['zoom'] = 11
        response = self.client.get(BRK_GEO_QUERY.format(urlencode(q)),
                                   **self.header_auth_scope_brk_plus)
        self.assertValidMatching(response)

        q['buurt_naam'] = 'Stationsplein e.o.'
        response = self.client.get(BRK_GEO_QUERY.format(urlencode(q)),
                                   **self.header_auth_scope_brk_plus)
        self.assertValidEmpty(response)

    def test_get_geodata_gebied_buurtcombinatie(self):
        q = {'eigenaar_cat': 'De staat', 'zoom': 14, 'bbox': brk.get_bbox_leaflet(), 'buurtcombinatie_naam': 'Grachtengordel-West'}
        response = self.client.get(BRK_GEO_QUERY.format(urlencode(q)),
                                   **self.header_auth_scope_brk_plus)
        self.assertValidEmpty(response)

        q['buurtcombinatie_naam'] = 'Burgwallen-Oude Zijde'
        response = self.client.get(BRK_GEO_QUERY.format(urlencode(q)),
                                   **self.header_auth_scope_brk_plus)
        self.assertValidMatching(response, zoomed_in=True)

        q['zoom'] = 11
        response = self.client.get(BRK_GEO_QUERY.format(urlencode(q)),
                                   **self.header_auth_scope_brk_plus)
        self.assertValidMatching(response)

        q['buurtcombinatie_naam'] = 'Grachtengordel-West'
        response = self.client.get(BRK_GEO_QUERY.format(urlencode(q)),
                                   **self.header_auth_scope_brk_plus)
        self.assertValidEmpty(response)

    def test_get_geodata_gebied_ggw(self):
        q = {'eigenaar_cat': 'De staat', 'zoom': 14, 'bbox': brk.get_bbox_leaflet(), 'ggw_naam': 'Centrum-Oost'}
        response = self.client.get(BRK_GEO_QUERY.format(urlencode(q)),
                                   **self.header_auth_scope_brk_plus)
        self.assertValidEmpty(response)

        q['ggw_naam'] = 'Centrum-West'
        response = self.client.get(BRK_GEO_QUERY.format(urlencode(q)),
                                   **self.header_auth_scope_brk_plus)
        self.assertValidMatching(response, zoomed_in=True)

        q['zoom'] = 11
        response = self.client.get(BRK_GEO_QUERY.format(urlencode(q)),
                                   **self.header_auth_scope_brk_plus)
        self.assertValidMatching(response)

        q['ggw_naam'] = 'Centrum-Oost'
        response = self.client.get(BRK_GEO_QUERY.format(urlencode(q)),
                                   **self.header_auth_scope_brk_plus)
        self.assertValidEmpty(response)

    @tag('geo')
    def test_get_geodata_gebied_stadsdeel(self):
        q = {'eigenaar_cat': 'De staat', 'zoom': 14, 'bbox': brk.get_bbox_leaflet(), 'stadsdeel_naam': 'Noord'}
        response = self.client.get(BRK_GEO_QUERY.format(urlencode(q)),
                                   **self.header_auth_scope_brk_plus)
        self.assertValidEmpty(response)

        q['stadsdeel_naam'] = 'Centrum'
        response = self.client.get(BRK_GEO_QUERY.format(urlencode(q)),
                                   **self.header_auth_scope_brk_plus)
        self.assertValidMatching(response, zoomed_in=True)

        q['zoom'] = 11
        response = self.client.get(BRK_GEO_QUERY.format(urlencode(q)),
                                   **self.header_auth_scope_brk_plus)
        self.assertValidMatching(response)

        q['stadsdeel_naam'] = 'Noord'
        response = self.client.get(BRK_GEO_QUERY.format(urlencode(q)),
                                   **self.header_auth_scope_brk_plus)
        self.assertValidEmpty(response)

    def assertValidMatching(self, response, zoomed_in=False, appartementen=False):
        self.assertEqual(response.status_code, 200)
        if zoomed_in:
            self.assertEqual(len(response.json()['appartementen']), 1)
        else:
            self.assertEqual(len(response.json()['appartementen']), 0)
        if not appartementen:
            self.assertGeoJSON(response.json()['eigenpercelen'])
        self.assertGeoJSON(response.json()['niet_eigenpercelen'])
        self.assertEqual(len(response.json()['extent']), 4)

    def assertValidEmpty(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['appartementen']), 0)
        self.assertIsNone(response.json()['eigenpercelen'])
        self.assertIsNone(response.json()['niet_eigenpercelen'])
        self.assertIsNone(response.json()['extent'])

    def assertGeoJSON(self, geojson):
        self.assertIsInstance(geojson, dict)
        self.assertIn('type', geojson)
        self.assertIn('coordinates', geojson)

    @tag('brk')
    def test_shape_parameter(self):
        fixture = {
            'shape': "[[4.890712,52.373579],[4.8920548,52.3736018],[4.8932629,52.3732028],"
                     "[4.8929459,52.3727335],[4.8906613,52.3727228]]"}
        result = modify_queryparams_for_shape(fixture)
        self.assertEqual(result, True)

        fixture = {'shape': "[]"}
        modify_queryparams_for_shape(fixture)
        self.assertNotIn('zoom', fixture)
        self.assertNotIn('shape', fixture)

    @tag('brk')
    def test_api_search(self):
        q = {}
        response = self.client.get(BRK_BASE_QUERY.format(urlencode(q)),
                                   **self.header_auth_scope_brk_plus)
        result = response.json()
        self.assertEqual(result['object_count'], 1)
        obj0 = result['object_list'][0]
        self.assertEqual(obj0['burgerlijke_gemeentenaam'], 'Amsterdam')
        self.assertEqual(obj0['aanduiding'], 'ASD10 S 00012 G 0023')
        agg_eigenaar_cat = result['aggs_list']['eigenaar_cat']
        self.assertEqual(agg_eigenaar_cat['buckets'][0]['key'], 'De staat')
        self.assertEqual(agg_eigenaar_cat['buckets'][0]['doc_count'], 1)

    @tag('brk')
    def test_api_search_with_shape(self):
        q = {'shape': "[[3.3135576333212353, 47.97476588287572],[3.3135390644506812, 47.975214773576475],[3.31420758007582, 47.97522724021333],[3.3142261429684208, 47.97477834935932]]"}
        response = self.client.get(BRK_BASE_QUERY.format(urlencode(q)),
                                   **self.header_auth_scope_brk_plus)
        result = response.json()
        self.assertEqual(result['object_count'], 1)
        obj0 = result['object_list'][0]
        self.assertEqual(obj0['burgerlijke_gemeentenaam'], 'Amsterdam')
        self.assertEqual(obj0['aanduiding'], 'ASD10 S 00012 G 0023')
        agg_eigenaar_cat = result['aggs_list']['eigenaar_cat']
        self.assertEqual(agg_eigenaar_cat['buckets'][0]['key'], 'De staat')
        self.assertEqual(agg_eigenaar_cat['buckets'][0]['doc_count'], 1)

        q = {'shape': "[[25.0,25.0],[25.0,75.0],[75.0,75.0],[75.0,25.0]]"}
        response = self.client.get(BRK_BASE_QUERY.format(urlencode(q)),
                                   **self.header_auth_scope_brk_plus)
        result = response.json()
        self.assertEqual(result['object_count'], 0)

    @tag('brk')
    def test_api_kot(self):
        response = self.client.get(BRK_KOT_QUERY, **self.header_auth_scope_brk_plus)
        result = response.json()
        self.assertEqual(result['object_count'], 1)
        obj0 = result['object_list'][0]
        self.assertEqual(obj0['aanduiding'], 'ASD10 S 00012 G 0023')

    @tag('brk')
    def test_api_kot_with_shape(self):
        q = {'shape': "[[3.3135576333212353, 47.97476588287572],[3.3135390644506812, 47.975214773576475],[3.31420758007582, 47.97522724021333],[3.3142261429684208, 47.97477834935932]]"}
        response = self.client.get(BRK_KOT_QUERY.format(urlencode(q)),
                                   **self.header_auth_scope_brk_plus)
        result = response.json()
        self.assertEqual(result['object_count'], 1)
        obj0 = result['object_list'][0]
        self.assertEqual(obj0['aanduiding'], 'ASD10 S 00012 G 0023')

        q = {'shape': "[[25.0,25.0],[25.0,75.0],[75.0,75.0],[75.0,25.0]]"}
        response = self.client.get(BRK_KOT_QUERY.format(urlencode(q)),
                                   **self.header_auth_scope_brk_plus)
        result = response.json()
        self.assertEqual(result['object_count'], 0)

    @tag('brk')
    def test_response_is_streaming(self):
        """Verify that the response is streaming"""
        response = self.client.get(BRK_EXPORT_QUERY, **self.header_auth_scope_brk_plus)
        self.assertTrue(response.streaming)

    @tag('brk')
    def test_complete_export_eigendommen(self):
        response = self.client.get(BRK_EXPORT_QUERY, **self.header_auth_scope_brk_plus)
        # assert that response status is 200
        self.assertEqual(response.status_code, 200)
        result = (b''.join(response.streaming_content)).decode('utf-8').strip()
        result = result.split('\r\n')
        # 2 lines: headers + 1 item
        self.assertEqual(len(result), 2)
        self.assertTrue('ASD10 S 00012 G 0023' in result[1])
        self.assertTrue('Amsterdam' in result[1])
        self.assertTrue('Postbus 123 1234AA Amsterdam' in result[1])


class FilterApiTest(ESTestCase, AuthorizationSetup):

    @classmethod
    def setUpTestData(cls):
        # super(ESTestCase, cls).setUpTestData()

        bag.create_gemeente_fixture()
        bag.create_buurt_combinaties()
        bag.create_buurt_fixtures()
        bag.create_gebiedsgericht_werken_fixtures()
        bag.create_stadsdeel_fixtures()

        create_brk_data()
        eigendom = brk.create_eigendom1()[0][0]
        cls.kot = eigendom.kadastraal_object
        log.info(cls.kot.stadsdelen.all())

        brk.create_geo_tables()
        cls.rebuild_elastic_index()

    def setUp(self):
        brk.create_geo_data(self.kot)

        self.client = Client()
        self.setup_authorization()

    @tag('brk')
    def test_api_search_filter1(self):
        '''
        Filter op Stadsdeel Noord. Dit geeft een resultaat dat in twee stadsdelen zit, maar omdat er
        gefilterd wordt op Noord in  in de aggregaties alleen Noord zichtbaar
        '''
        q = {'stadsdeel_naam': 'Noord'}
        response = self.client.get(BRK_BASE_QUERY.format(urlencode(q)),
                                   **self.header_auth_scope_brk_plus)
        result = response.json()
        self.assertEqual(result['object_count'], 1)
        obj0 = result['object_list'][0]
        self.assertEqual(obj0['burgerlijke_gemeentenaam'], 'Amsterdam')
        self.assertEqual(obj0['aanduiding'], 'ASD10 S 00012 G 0023')
        agg_eigenaar_cat = result['aggs_list']['eigenaar_cat']
        self.assertEqual(agg_eigenaar_cat['buckets'][0]['key'], 'De staat')
        self.assertEqual(agg_eigenaar_cat['buckets'][0]['doc_count'], 1)
        agg_stadsdeel_naam = result['aggs_list']['stadsdeel_naam']
        self.assertEqual(len(agg_stadsdeel_naam['buckets']), 1)
        self.assertEqual(agg_stadsdeel_naam['buckets'][0]['key'], 'Noord')
        self.assertEqual(agg_stadsdeel_naam['buckets'][0]['doc_count'], 1)


    @tag('brk')
    def test_api_search_filter2(self):
        q = {'stadsdeel_naam': 'Oost'}
        response = self.client.get(BRK_BASE_QUERY.format(urlencode(q)),
                               **self.header_auth_scope_brk_plus)
        result = response.json()
        self.assertEqual(result['object_count'], 0)

class FilterApiTestMultipleOutput(ESTestCase, AuthorizationSetup):

    @classmethod
    def setUpTestData(cls):
        create_brk_data()
        # create 10 objects in the database
        eigendom = brk.create_eigendommen(10)
        cls.kots = [kot[0].kadastraal_object for kot in eigendom]
        brk.create_geo_tables()
        cls.rebuild_elastic_index()

    def test_api_search_filter_size(self):
        """Prove that size param returns number of objects specified
        """
        q = {'size': '5'}
        self.client = Client()
        self.setup_authorization()
        response = self.client.get(BRK_BASE_QUERY.format(urlencode(q)),
                                    **self.header_auth_scope_brk_plus)
        result = response.json()
        num_of_objects =  len(result['object_list'])
        self.assertEqual(num_of_objects, 5)
        self.assertEqual(result['page_count'], 2)
        self.assertEqual(result['object_count'], 10)
