# Packages
from django.contrib.gis.geos import Polygon, Point

from datasets.bag import models
from .fixtures_geometrie import gebied_geometrie


def create_stadsdeel_fixtures():
    """
    depends on gemeente
    :return: A list of stadsdeel fixtures
    """
    return [
        models.Stadsdeel.objects.get_or_create(
            id="03630000000018", code="A", naam="Centrum", vervallen=False,
            gemeente_id="03630000000000", geometrie=gebied_geometrie['03630000000018']
        ),
        models.Stadsdeel.objects.get_or_create(
            id="03630000000019", code="N", naam="Noord", vervallen=False,
            gemeente_id="03630000000000", geometrie=gebied_geometrie['noord']
        ),
    ]


def create_gebiedsgericht_werken_fixtures():
    """
    depends on stadssdeel fixtures
    :return: a list of gebieds_gericht_werken objects
    """
    create_stadsdeel_fixtures()
    create_ggw = models.Gebiedsgerichtwerken.objects.get_or_create
    return [
        create_ggw(id="DX01", naam="Centrum-West", code="DX01",
                   stadsdeel_id="03630000000018", geometrie=gebied_geometrie['DX01']),
        create_ggw(id="DX02", naam="Centrum-Oost", code="DX02",
                   stadsdeel_id="03630000000018", geometrie=gebied_geometrie['off']),
    ]


def create_grootstedelijk_werken_fixtures():
    """
    """
    pass


def create_buurt_combinaties():
    """"
    """
    create_stadsdeel_fixtures()
    create_bc = models.Buurtcombinatie.objects.get_or_create
    return [
        create_bc(id="3630012052028", naam="Grachtengordel-West", code="02",
                  vollcode="A02", stadsdeel_id="03630000000018",
                  geometrie=gebied_geometrie['off']),
        create_bc(id="3630012052029", naam="Haarlemmerbuurt", code="05",
                  vollcode="A05", stadsdeel_id="03630000000018"),
        create_bc(id="3630012052031", naam="Weesperbuurt/Plantage", code="08",
                  vollcode="A08", stadsdeel_id="03630000000018"),
        create_bc(id="3630012052032", naam="De Weteringschans", code="07",
                  vollcode="A07", stadsdeel_id="03630000000018"),
        create_bc(id="3630012052033", naam="Nieuwmarkt/Lastage", code="04",
                  vollcode="A04", stadsdeel_id="03630000000018"),
        create_bc(id="3630012052034", naam="Grachtengordel-Zuid", code="03",
                  vollcode="A03", stadsdeel_id="03630000000018"),
        create_bc(id="3630012052035", naam="Burgwallen-Nieuwe Zijde", code="01",
                  vollcode="A01", stadsdeel_id="03630000000018"),
        create_bc(id='3630012052036', naam="Burgwallen-Oude Zijde", code="00",
                  vollcode="A00", stadsdeel_id="03630000000018",
                  geometrie=gebied_geometrie['3630012052036']),
        create_bc(id="3630012052037", naam="Jordaan", code="06",
                  vollcode="A06", stadsdeel_id="03630000000018"),
    ]


def create_buurt_fixtures():
    """
    depends on stadsdeel and buurtcombinatie

    :return: A list of buurt fixtures
    """
    create_stadsdeel_fixtures()
    create_buurt = models.Buurt.objects.get_or_create
    return [
        create_buurt(code="01a", vollcode="A01a", naam="Stationsplein e.o.",
                     vervallen=False, geometrie=gebied_geometrie['01a'],
                     buurtcombinatie_id="3630012052035",
                     stadsdeel_id="03630000000018", id="1"),
        create_buurt(code="01b", vollcode="A01b", naam="Hemelrijk",
                     vervallen=False, geometrie=gebied_geometrie['01b'],
                     buurtcombinatie_id="3630012052035",
                     stadsdeel_id="03630000000018", id="2"),
        create_buurt(code="01c", vollcode="A01c", naam="Nieuwendijk Noord",
                     vervallen=False, geometrie=gebied_geometrie['01c'],
                     buurtcombinatie_id="3630012052035",
                     stadsdeel_id="03630000000018", id="3"),
        create_buurt(code="01d", vollcode="A01d", naam="Spuistraat Noord",
                     vervallen=False, geometrie=gebied_geometrie['01d'],
                     buurtcombinatie_id="3630012052035",
                     stadsdeel_id="03630000000018", id="4"),
        create_buurt(code="01e", vollcode="A01e", naam="Nieuwe Kerk e.o.",
                     vervallen=False, geometrie=gebied_geometrie['01e'],
                     buurtcombinatie_id="3630012052035",
                     stadsdeel_id="03630000000018", id="5"),
        create_buurt(code="01f", vollcode="A01f", naam="Spuistraat Zuid",
                     vervallen=False, geometrie=gebied_geometrie['01f'],
                     buurtcombinatie_id="3630012052035",
                     stadsdeel_id="03630000000018", id="6"),
        create_buurt(code="01g", vollcode="A01g", naam="Begijnhofbuurt",
                     vervallen=False, geometrie=gebied_geometrie['01g'],
                     buurtcombinatie_id="3630012052035",
                     stadsdeel_id="03630000000018", id="7"),
        create_buurt(code="01h", vollcode="A01h", naam="Kalverdriehoek",
                     vervallen=False, geometrie=gebied_geometrie['01h'],
                     buurtcombinatie_id="3630012052035",
                     stadsdeel_id="03630000000018", id="8"),
        create_buurt(code="02a", vollcode="A02a", naam="Langestraat e.o.",
                     vervallen=False, geometrie=gebied_geometrie['02a'],
                     buurtcombinatie_id="3630012052028",
                     stadsdeel_id="03630000000018", id="9"),
        create_buurt(code="02b", vollcode="A02b", naam="Leliegracht e.o.",
                     vervallen=False, geometrie=gebied_geometrie['02b'],
                     buurtcombinatie_id="3630012052028",
                     stadsdeel_id="03630000000018", id="10"),
        create_buurt(code="02c", vollcode="A02c", naam="Felix Meritisbuurt",
                     vervallen=False, geometrie=gebied_geometrie['02c'],
                     buurtcombinatie_id="3630012052028",
                     stadsdeel_id="03630000000018", id="11"),
        create_buurt(code="02d", vollcode="A02d", naam="Leidsegracht Noord",
                     vervallen=False, geometrie=gebied_geometrie['02d'],
                     buurtcombinatie_id="3630012052028",
                     stadsdeel_id="03630000000018", id="12"),
        create_buurt(code="00e", vollcode="A00e", naam="BG-terrein e.o.",
                     vervallen=False, geometrie=gebied_geometrie['00e'],
                     buurtcombinatie_id="3630012052036",
                     stadsdeel_id="03630000000018", id="20"),
    ]


def create_status_fixtures():
    """
    returms a list with status fixtures
    :return:
    """
    return ['Ligplaats aangewezen', 'Naamgeving uitgegeven', 'Standplaats toegewezen']


def create_gemeente_fixture():
    """

    :return: returns a list with a gemeente fixture
    """
    return [
        models.Gemeente.objects.get_or_create(
            id='03630000000000', code='0363',
            naam='Amsterdam',
            verzorgingsgebied=True,
            vervallen=False)]


def create_woonplaats_fixture():
    """
    depends on gemeente fixture

    :return: List with woonplaats fixture
    """
    return [
        models.Woonplaats.objects.get_or_create(
            id='03630022796658',
            landelijk_id='3594',
            naam='Amsterdam',
            gemeente_id='03630000000000',
            vervallen=False)]


def create_openbare_ruimte_fixtures():
    """
    depends on woonplaats_fixture, status_fixture
    :return: list of openbare_ruimte objects.
    """
    create_status_fixtures()
    create_woonplaats_fixture()

    return [
        models.OpenbareRuimte.objects.get_or_create(
            id='03630000000001',
            landelijk_id='0363000000000001',
            woonplaats_id='03630022796658',
            naam='Kanaalstraat',
            status='Naamgeving uitgegeven'),
        models.OpenbareRuimte.objects.get_or_create(
            id='03630000000002',
            landelijk_id='0363000000000002',
            woonplaats_id='03630022796658',
            naam='Leidsestraat',
            status='Naamgeving uitgegeven'),

        models.OpenbareRuimte.objects.get_or_create(
            id='03630000000003',
            landelijk_id='0363000000000003',
            woonplaats_id='03630022796658',
            naam='Hobbemakade',
            status='Naamgeving uitgegeven'),

        models.OpenbareRuimte.objects.get_or_create(
            id='03630000000004',
            landelijk_id='0363000000000004',
            woonplaats_id='03630022796658',
            naam='Delflandplein',
            status='Naamgeving uitgegeven'),

        models.OpenbareRuimte.objects.get_or_create(
            id='03630000000005',
            landelijk_id='0363000000000005',
            woonplaats_id='03630022796658',
            naam='Vriesseveem',
            status='Naamgeving uitgegeven'),

        models.OpenbareRuimte.objects.get_or_create(
            id='03630000000006',
            landelijk_id='0363000000000006',
            woonplaats_id='03630022796658',
            naam='Hoofddorplein',
            status='Naamgeving uitgegeven'),

        models.OpenbareRuimte.objects.get_or_create(
            id='03630000000007',
            landelijk_id='0363000000000007',
            woonplaats_id='03630022796658',
            naam='Prinsengracht',
            status='Naamgeving uitgegeven'),

        models.OpenbareRuimte.objects.get_or_create(
            id='03630000000008',
            landelijk_id='0363000000000008',
            woonplaats_id='03630022796658',
            naam='Weteringschans',
            status='Naamgeving uitgegeven'),

        models.OpenbareRuimte.objects.get_or_create(
            id='03630000000009',
            landelijk_id='0363000000000009',
            woonplaats_id='03630022796658',
            naam='Stapels',
            status='Naamgeving uitgegeven'),

        models.OpenbareRuimte.objects.get_or_create(
            id='03630000000010',
            landelijk_id='0363000000000010',
            woonplaats_id='03630022796658',
            naam='Delflandplein',
            status='Naamgeving uitgegeven')]


def create_verblijfsobject_fixtures():
    create_buurt_fixtures()
    # create_gebruiksdoelen

    verblijfsobjecten = [
        models.Verblijfsobject.objects.get_or_create(
            id="03630000543292",
            landelijk_id="0363010000543292",
            oppervlakte=30,
            aantal_kamers=0,
            vervallen=0,
            _openbare_ruimte_naam="Eerste Anjeliersdwarsstraat",
            _huisnummer=1,
            _huisletter='',
            _huisnummer_toevoeging="H",
            buurt_id="1",
            geometrie=Point(1000, 1000),
            gebruiksdoel=["BEST-woning",],
            toegang=["Trap"],
        ),
        models.Verblijfsobject.objects.get_or_create(
            id="03630000543293",
            landelijk_id="0363010000543293",
            oppervlakte=32,
            aantal_kamers=2,
            vervallen=0,
            _openbare_ruimte_naam="Kanaalstraat",
            _huisnummer=1,
            _huisletter='A',
            _huisnummer_toevoeging='BIS',
            buurt_id="1",
            geometrie=Point(3, 3),
            gebruiksdoel=["BEST-winkelfunctie",],
            toegang=["Trap"],
        ),
        models.Verblijfsobject.objects.get_or_create(
            id="03630000543294",
            landelijk_id="0363010000543294",
            oppervlakte=48,
            aantal_kamers=2,
            vervallen=0,
            _openbare_ruimte_naam="Leidsestraat",
            _huisnummer=15,
            _huisletter='',
            _huisnummer_toevoeging="",
            buurt_id="2",
            geometrie=Point(100, 150),
            gebruiksdoel=["BEST-winkelfunctie",],
            toegang=["Trap"],
        ),
        models.Verblijfsobject.objects.get_or_create(
            id="03630000543295",
            landelijk_id="0363010000543295",
            oppervlakte=48,
            aantal_kamers=2,
            vervallen=0,
            _openbare_ruimte_naam="Leidsestraat",
            _huisnummer=15,
            _huisletter='',
            _huisnummer_toevoeging="",
            buurt_id="2",
            geometrie=Point(150, 100),
            gebruiksdoel=["BEST-woning",],
            toegang=["Trap"],
        ),
        models.Verblijfsobject.objects.get_or_create(
            id="03630000543296",
            landelijk_id="0363010000543296",
            oppervlakte=32,
            aantal_kamers=2,
            vervallen=0,
            _openbare_ruimte_naam="Hobbemakade",
            _huisnummer=12,
            _huisletter='',
            _huisnummer_toevoeging="",
            buurt_id="3",
            geometrie=Point(100, 100),
            gebruiksdoel=["BEST-woning",],
            toegang=["Trap"],
        ),
        models.Verblijfsobject.objects.get_or_create(
            id="03630000543297",
            landelijk_id="0363010000543297",
            oppervlakte=30,
            aantal_kamers=0,
            vervallen=0,
            _openbare_ruimte_naam="Eerste Anjeliersdwarsstraat",
            _huisnummer=1,
            _huisletter='',
            _huisnummer_toevoeging="H",
            buurt_id="4",
            geometrie=Point(100, 100),
            gebruiksdoel=["BEST-woning",],
            toegang=["Trap"],
        ),
        models.Verblijfsobject.objects.get_or_create(
            id="03630000543298",
            landelijk_id="0363010000543298",
            oppervlakte=32,
            aantal_kamers=2,
            vervallen=0,
            _openbare_ruimte_naam="Eerste Anjeliersdwarsstraat",
            _huisnummer=1,
            _huisletter='',
            _huisnummer_toevoeging="1",
            buurt_id="5",
            geometrie=Point(20, 30),
            gebruiksdoel=["BEST-woning",],
            toegang=["Trap"],
        ),
        models.Verblijfsobject.objects.get_or_create(
            id="03630000543299",
            landelijk_id="0363010000543299",
            oppervlakte=48,
            aantal_kamers=2,
            vervallen=0,
            _openbare_ruimte_naam="Eerste Anjeliersdwarsstraat",
            _huisnummer=1,
            _huisletter='',
            _huisnummer_toevoeging="2",
            buurt_id="6",
            geometrie=Point(100, 100),
            gebruiksdoel=["BEST-woning",],
            toegang=["Trap"],
        ),
        models.Verblijfsobject.objects.get_or_create(
            id="03630000543291",
            landelijk_id="0363010000543291",
            oppervlakte=32,
            aantal_kamers=2,
            vervallen=0,
            _openbare_ruimte_naam="Eerste Anjeliersdwarsstraat",
            _huisnummer=3,
            _huisletter='',
            _huisnummer_toevoeging="1",
            buurt_id="7",
            geometrie=Point(30, 20),
            gebruiksdoel=["BEST-woning",],
            toegang=["Trap"],
        ),
    ]

    return verblijfsobjecten


def create_ligplaats_fixtures():
    """

    :return: a list of ligplaats objects
    """
    create_buurt_fixtures()
    return [
        models.Ligplaats.objects.get_or_create(
            id='03630000000111', landelijk_id='0363000000000111',
            status='Ligplaats aangewezen',
            _huisnummer=15, _huisletter='', _huisnummer_toevoeging='',
            buurt_id='2',
            geometrie=Polygon(
                (
                    (0.0, 0.0),
                    (0.0, 50.0),
                    (50.0, 50.0),
                    (50.0, 0.0),
                    (0.0, 0.0)
                )
            )),

        models.Ligplaats.objects.get_or_create(
            id='03630000000112', landelijk_id='0363000000000112',
            status='Ligplaats aangewezen',
            _huisnummer=345, _huisletter='', _huisnummer_toevoeging='',
            buurt_id='3',
            geometrie=Polygon(
                (
                    (0.0, 0.0),
                    (0.0, 50.0),
                    (50.0, 50.0),
                    (50.0, 0.0),
                    (0.0, 0.0)
                )
            ))]


def create_standplaats_fixtures():
    """
    :return: a list of standplaats objects
    """
    create_buurt_fixtures()

    return [
        models.Standplaats.objects.get_or_create(
            id='03630000000221', landelijk_id='0363000000000221',
            status='Standplaats toegewezen',
            _huisnummer=515, _huisletter='', _huisnummer_toevoeging='',
            buurt_id='10', geometrie=Polygon(
                (
                    (0.0, 0.0),
                    (0.0, 50.0),
                    (50.0, 50.0),
                    (50.0, 0.0),
                    (0.0, 0.0)
                )
            )),

        models.Standplaats.objects.get_or_create(
            id='03630000000222', landelijk_id='0363000000000222',
            status='Standplaats toegewezen',
            _huisnummer=45, _huisletter='', _huisnummer_toevoeging='',
            buurt_id='9', geometrie=Polygon(
                (
                    (0.0, 0.0),
                    (0.0, 50.0),
                    (50.0, 50.0),
                    (50.0, 0.0),
                    (0.0, 0.0)
                )
            ))]


def create_nummeraanduiding_fixtures():
    """
    depends on openbare_ruimte_fixtures,
    verblijfsobject_fixtures, standplaats_fixtures and
    ligplaats_fixtures
    :return: a list of nummeraanduiding objects
    """

    create_gemeente_fixture()
    create_gebiedsgericht_werken_fixtures()
    create_grootstedelijk_werken_fixtures()
    create_openbare_ruimte_fixtures()
    create_buurt_combinaties()
    create_buurt_fixtures()
    create_verblijfsobject_fixtures()
    create_ligplaats_fixtures()
    create_standplaats_fixtures()

    # Dropping the creatd bool from the get_or_create
    nummeraanduidingen = [
        models.Nummeraanduiding.objects.get_or_create(
            huisnummer=1,
            huisletter='A',
            huisnummer_toevoeging='BIS',
            postcode='1012AA',
            type='01',
            landelijk_id='0363000000000001',
            openbare_ruimte_id='03630000000001',
            id='03630000000001',
            verblijfsobject_id='03630000543293',
            _openbare_ruimte_naam='Kanaalstraat')[0],

        models.Nummeraanduiding.objects.get_or_create(
            huisnummer=15,
            huisletter='',
            huisnummer_toevoeging='',
            postcode='1012AA',
            type='01',
            landelijk_id='0363000000000002',
            openbare_ruimte_id='03630000000002',
            id='03630000000002',
            verblijfsobject_id='03630000543294',
            _openbare_ruimte_naam='Leidsestraat')[0],
        models.Nummeraanduiding.objects.get_or_create(
            huisnummer=12,
            huisletter='',
            huisnummer_toevoeging=' ',
            postcode='1012AA',
            type='01',
            landelijk_id='0363000000000003',
            openbare_ruimte_id='03630000000003',
            id='03630000000003',
            verblijfsobject_id='03630000543295',
            _openbare_ruimte_naam='Hobbemakade')[0],

        models.Nummeraanduiding.objects.get_or_create(
            huisnummer=15,
            huisletter='C',
            huisnummer_toevoeging='2',
            postcode='1012AB',
            type='01',
            landelijk_id='0363000000000004',
            openbare_ruimte_id='03630000000004',
            id='03630000000004',
            ligplaats_id='03630000000111',
            _openbare_ruimte_naam='Delflandplein')[0],

        models.Nummeraanduiding.objects.get_or_create(
            huisnummer=21,
            huisletter='',
            huisnummer_toevoeging='',
            postcode='1012AA',
            type='01',
            landelijk_id='0363000000000005',
            openbare_ruimte_id='03630000000005',
            id='03630000000005',
            verblijfsobject_id='03630000543296',
            _openbare_ruimte_naam='Hoofddorplein')[0],

        models.Nummeraanduiding.objects.get_or_create(
            huisnummer=345,
            huisletter='',
            huisnummer_toevoeging='1',
            postcode='1012AA',
            type='01',
            landelijk_id='0363000000000006',
            openbare_ruimte_id='03630000000006',
            id='03630000000006',
            ligplaats_id='03630000000112',
            _openbare_ruimte_naam='Hoofddorplein')[0],

        models.Nummeraanduiding.objects.get_or_create(
            huisnummer=76,
            huisletter='F',
            huisnummer_toevoeging='',
            postcode='1013AG',
            type='01',
            landelijk_id='0363000000000007',
            openbare_ruimte_id='03630000000007',
            id='03630000000007',
            verblijfsobject_id='03630000543297',
            _openbare_ruimte_naam='Prinsengracht')[0],

        models.Nummeraanduiding.objects.get_or_create(
            huisnummer=515,
            huisletter='',
            huisnummer_toevoeging='',
            postcode='1013BA',
            type='01',
            landelijk_id='0363000000000008',
            openbare_ruimte_id='03630000000008',
            id='03630000000008',
            standplaats_id='03630000000221',
            _openbare_ruimte_naam='Weteringschans')[0],

        models.Nummeraanduiding.objects.get_or_create(
            huisnummer=45,
            huisletter='',
            huisnummer_toevoeging='',
            postcode='1014AZ',
            type='01',
            landelijk_id='0363000000000009',
            openbare_ruimte_id='03630000000009',
            id='03630000000009',
            standplaats_id='03630000000222',
            _openbare_ruimte_naam='Delflandplein')[0],

        models.Nummeraanduiding.objects.get_or_create(
            huisnummer=4,
            huisletter='',
            huisnummer_toevoeging='',
            postcode='1014AW',
            type='01',
            landelijk_id='0363000000000010',
            openbare_ruimte_id='03630000000009',
            id='03630000000010',
            verblijfsobject_id='03630000543298',
            _openbare_ruimte_naam='Delflandplein')[0]
    ]

    return nummeraanduidingen
