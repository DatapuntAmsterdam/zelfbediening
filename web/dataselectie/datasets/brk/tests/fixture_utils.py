import logging
import json

import factory
from factory import fuzzy
import faker
from datasets.brk import models
from django.db import connection
from django.contrib.gis.geos import MultiPolygon, Polygon, Point
from datasets.brk import geo_models
from datasets.brk import models
from datasets.brk.management import brk_batch_sql
from datasets.generic import kadaster
from .fixtures_geometrie import perceel_geometrie

log = logging.getLogger(__name__)

SRID_WSG84 = 4326
SRID_RD = 28992

f = faker.Factory.create(locale='nl_NL')

def random_poly():
    return MultiPolygon(
        Polygon(
            ((0.0, 0.0), (0.0, 50.0), (50.0, 50.0), (50.0, 0.0), (0.0, 0.0))))

class GemeenteFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Gemeente
        django_get_or_create = ('gemeente', )

    gemeente = factory.LazyAttribute(lambda o: f.city())
    geometrie = random_poly()


class KadastraleGemeenteFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.KadastraleGemeente

    pk = fuzzy.FuzzyText(length=5)
    gemeente = factory.SubFactory(GemeenteFactory)
    geometrie = random_poly()


class KadastraleSectieFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.KadastraleSectie

    pk = fuzzy.FuzzyText(length=60)
    sectie = fuzzy.FuzzyText(length=1)
    kadastrale_gemeente = factory.SubFactory(KadastraleGemeenteFactory)
    geometrie = random_poly()


class KadastraalObjectFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.KadastraalObject

    pk = fuzzy.FuzzyText(length=60)
    aanduiding = factory.LazyAttribute(
        lambda obj: kadaster.get_aanduiding(
            obj.kadastrale_gemeente.id,
            obj.sectie.sectie,
            obj.perceelnummer,
            obj.indexletter,
            obj.indexnummer))

    kadastrale_gemeente = factory.SubFactory(KadastraleGemeenteFactory)
    sectie = factory.SubFactory(KadastraleSectieFactory)
    perceelnummer = fuzzy.FuzzyInteger(low=0, high=9999)
    indexletter = fuzzy.FuzzyChoice(choices=('A', 'G'))
    indexnummer = fuzzy.FuzzyInteger(low=0, high=9999)
    grootte = fuzzy.FuzzyInteger(low=10, high=1000)
    register9_tekst = fuzzy.FuzzyText(length=50)
    poly_geom = random_poly()


class AdresFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Adres

    pk = fuzzy.FuzzyText(length=32)
    openbareruimte_naam = fuzzy.FuzzyText(length=80)


# class NatuurlijkPersoonFactory(factory.DjangoModelFactory):
#     class Meta:
#         model = models.KadastraalSubject
#
#     pk = fuzzy.FuzzyText(length=60)
#     type = models.KadastraalSubject.SUBJECT_TYPE_NATUURLIJK
#     bron = fuzzy.FuzzyChoice(
#         choices=(models.KadastraalSubject.BRON_KADASTER,
#                  models.KadastraalSubject.BRON_REGISTRATIE))
#     woonadres = factory.SubFactory(AdresFactory)
#     postadres = factory.SubFactory(AdresFactory)
#
#
# class NietNatuurlijkPersoonFactory(factory.DjangoModelFactory):
#     class Meta:
#         model = models.KadastraalSubject
#
#     pk = fuzzy.FuzzyText(length=60)
#     type = models.KadastraalSubject.SUBJECT_TYPE_NIET_NATUURLIJK
#     bron = fuzzy.FuzzyChoice(choices=(
#         models.KadastraalSubject.BRON_KADASTER,
#         models.KadastraalSubject.BRON_REGISTRATIE))
#     woonadres = factory.SubFactory(AdresFactory)
#     postadres = factory.SubFactory(AdresFactory)


class EigenaarFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Eigenaar

    pk = fuzzy.FuzzyText(length=60)
    type = fuzzy.FuzzyChoice(
            choices=(models.Eigenaar.SUBJECT_TYPE_NATUURLIJK,
                     models.Eigenaar.SUBJECT_TYPE_NIET_NATUURLIJK))
    bron = fuzzy.FuzzyChoice(
            choices=(models.Eigenaar.BRON_KADASTER,
                     models.Eigenaar.BRON_REGISTRATIE))
    woonadres = factory.SubFactory(AdresFactory)
    postadres = factory.SubFactory(AdresFactory)


class AardZakelijkRechtFactory(factory.DjangoModelFactory):

    pk = fuzzy.FuzzyText(length=10)

    class Meta:
        model = models.AardZakelijkRecht


class ZakelijkRechtFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.ZakelijkRecht

    pk = fuzzy.FuzzyText(length=60)
    kadastraal_object = factory.SubFactory(KadastraalObjectFactory)
    kadastraal_subject = factory.SubFactory(EigenaarFactory)

    _kadastraal_subject_naam = fuzzy.FuzzyText(length=50)
    kadastraal_object_status = fuzzy.FuzzyText(length=50)
    aard_zakelijk_recht = factory.SubFactory(AardZakelijkRechtFactory)


def create_kadastraal_object():
    """
    depends on kadastrale gemeente / kadastrale sectie
    :return: A list of kot fixtures
    """

    gemeente = GemeenteFactory(
        gemeente='SunCity',
    )

    kadastrale_gemeente = KadastraleGemeenteFactory(
        pk='AX001',
        gemeente=gemeente,
        naam='SunCity',
    )

    sectie = KadastraleSectieFactory(
        sectie='S'
    )

    return KadastraalObjectFactory(
            kadastrale_gemeente=kadastrale_gemeente,
            perceelnummer=12,  # must be 5 long!
            indexletter='G',
            indexnummer=23,
            sectie=sectie,
            soort_grootte_id='SBCD',
            register9_tekst='12345789',
            status_code='X3'
        )


def create_eigendom():
    """
    depends on kadastraal object and categroie fixtures
    :return: a list of eigendom objects
    """
    create_eigenaar_categorie()
    kadastraal_object = create_kadastraal_object()
    kadastraal_subject = EigenaarFactory.create()
    zakelijkrecht = ZakelijkRechtFactory.create()

    return [

        models.Eigendom.objects.get_or_create(
            zakelijk_recht=zakelijkrecht,
            kadastraal_subject=kadastraal_subject,
            kadastraal_object=kadastraal_object,
            eigenaar_categorie_id=3,
            grondeigenaar=True,
            aanschrijfbaar=False,
            appartementeigenaar=False
        )
    ]


def create_eigenaar_categorie():
    return [
        models.EigenaarCategorie.objects.get_or_create(
            id=3,
            categorie='De staat',
        )
    ]


def create_geo_tables():
    with connection.cursor() as c:
        for sql_command in brk_batch_sql.dataselection_sql_commands \
                           + brk_batch_sql.mapselection_sql_commands:
            c.execute(sql_command)


def create_appartementen():
    return [
        geo_models.Appartementen.objects.get_or_create(
            id=1,
            cat_id=3,
            geometrie=Point(4.895, 52.368, srid=SRID_WSG84),
        )
    ]


def create_eigenpercelen():
    return [
        geo_models.EigenPerceel.objects.get_or_create(
            id=1,
            cat_id=3,
            geometrie=perceel_geometrie[1],
        ),
    ]


def create_eigenperceelgroepen():
    objects = []
    id = 0

    for category in [3, 99]:
        for eigendom_cat in [1, 9]:
            for gebied in [('buurt', '20'), ('wijk', '3630012052036'),
                           ('ggw', 'DX01'), ('stadsdeel', '03630000000018')]:
                id += 1
                objects.append(
                    geo_models.EigenPerceelGroep.objects.get_or_create(
                        id=id,
                        cat_id=category,
                        eigendom_cat=eigendom_cat,
                        gebied=gebied[0],
                        gebied_id=gebied[1],
                        geometrie=perceel_geometrie[1],
                    )
                )

    return objects


def create_niet_eigenpercelen():
    return [
        geo_models.NietEigenPerceel.objects.get_or_create(
            id=1,
            cat_id=3,
            geometrie=perceel_geometrie[2],
        )
    ]


def create_niet_eigenperceelgroepen():
    objects = []
    id = 0

    for category in [3, 99]:
        for eigendom_cat in [3, 9]:
            for gebied in [('buurt', '20'), ('wijk', '3630012052036'),
                           ('ggw', 'DX01'), ('stadsdeel', '03630000000018')]:
                id += 1
                objects.append(
                    geo_models.NietEigenPerceelGroep.objects.get_or_create(
                        id=id,
                        cat_id=category,
                        eigendom_cat=eigendom_cat,
                        gebied=gebied[0],
                        gebied_id=gebied[1],
                        geometrie=perceel_geometrie[2],
                    )
                )

    return objects


def create_geo_data():
    create_appartementen()
    create_eigenpercelen()
    create_eigenperceelgroepen()
    create_niet_eigenpercelen()
    create_niet_eigenperceelgroepen()


def get_bbox_leaflet():
    # get the leaflet-like LatLngBounds
    return json.dumps({
        '_northEast': {
            'lat': 52.37068,
            'lng': 4.894825
        },
        '_southWest': {
            'lat': 52.367797,
            'lng': 4.898945
        }
    })


def get_bbox():
    #   Left, top, right, bottom
    #       code expects WSG84, if it is easier in the frontend this can change to RD
    return '4.894825,52.370680,4.898945,52.367797'