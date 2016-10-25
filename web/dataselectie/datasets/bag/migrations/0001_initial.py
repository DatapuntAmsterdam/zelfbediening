# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-10-17 10:00
from __future__ import unicode_literals
from typing import Tuple
import datasets.bag.models
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []  # type: List[Tuple[str, str]]

    operations = [
        migrations.CreateModel(
            name='Bouwblok',
            fields=[
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('begin_geldigheid', models.DateField(null=True)),
                ('einde_geldigheid', models.DateField(null=True)),
                ('geometrie', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=28992)),
                ('id', models.CharField(max_length=14, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=4, unique=True)),
                ('ingang_cyclus', models.DateField(null=True)),
            ],
            options={
                'verbose_name': 'Bouwblok',
                'ordering': ('code',),
                'verbose_name_plural': 'Bouwblokken',
            },
        ),
        migrations.CreateModel(
            name='Buurt',
            fields=[
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('begin_geldigheid', models.DateField(null=True)),
                ('einde_geldigheid', models.DateField(null=True)),
                ('geometrie', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=28992)),
                ('id', models.CharField(max_length=14, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=3, unique=True)),
                ('vollcode', models.CharField(max_length=4)),
                ('naam', models.CharField(max_length=40)),
                ('vervallen', models.NullBooleanField(default=None)),
                ('ingang_cyclus', models.DateField(null=True)),
                ('brondocument_naam', models.CharField(max_length=100, null=True)),
                ('brondocument_datum', models.DateField(null=True)),
            ],
            options={
                'verbose_name': 'Buurt',
                'ordering': ('vollcode',),
                'verbose_name_plural': 'Buurten',
            },
        ),
        migrations.CreateModel(
            name='Buurtcombinatie',
            fields=[
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('begin_geldigheid', models.DateField(null=True)),
                ('einde_geldigheid', models.DateField(null=True)),
                ('id', models.CharField(max_length=14, primary_key=True, serialize=False)),
                ('naam', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=2)),
                ('vollcode', models.CharField(max_length=3)),
                ('brondocument_naam', models.CharField(max_length=100, null=True)),
                ('brondocument_datum', models.DateField(null=True)),
                ('ingang_cyclus', models.DateField(null=True)),
                ('geometrie', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=28992)),
            ],
            options={
                'verbose_name': 'Buurtcombinatie',
                'ordering': ('code',),
                'verbose_name_plural': 'Buurtcombinaties',
            },
        ),
        migrations.CreateModel(
            name='Eigendomsverhouding',
            fields=[
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('omschrijving', models.CharField(max_length=150, null=True)),
            ],
            options={
                'verbose_name': 'Eigendomsverhouding',
                'verbose_name_plural': 'Eigendomsverhoudingen',
            },
        ),
        migrations.CreateModel(
            name='Financieringswijze',
            fields=[
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('omschrijving', models.CharField(max_length=150, null=True)),
            ],
            options={
                'verbose_name': 'Financieringswijze',
                'verbose_name_plural': 'Financieringswijzes',
            },
        ),
        migrations.CreateModel(
            name='Gebiedsgerichtwerken',
            fields=[
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('id', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=4)),
                ('naam', models.CharField(max_length=100)),
                ('geometrie', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=28992)),
            ],
            options={
                'verbose_name': 'Gebiedsgerichtwerken',
                'ordering': ('code',),
                'verbose_name_plural': 'Gebiedsgerichtwerken',
            },
        ),
        migrations.CreateModel(
            name='Gebruik',
            fields=[
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('omschrijving', models.CharField(max_length=150, null=True)),
            ],
            options={
                'verbose_name': 'Gebruik',
                'verbose_name_plural': 'Gebruik',
            },
        ),
        migrations.CreateModel(
            name='Gemeente',
            fields=[
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('begin_geldigheid', models.DateField(null=True)),
                ('einde_geldigheid', models.DateField(null=True)),
                ('id', models.CharField(max_length=14, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=4, unique=True)),
                ('naam', models.CharField(max_length=40)),
                ('verzorgingsgebied', models.NullBooleanField(default=None)),
                ('vervallen', models.NullBooleanField(default=None)),
            ],
            options={
                'verbose_name': 'Gemeente',
                'verbose_name_plural': 'Gemeentes',
            },
        ),
        migrations.CreateModel(
            name='Grootstedelijkgebied',
            fields=[
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('id', models.SlugField(max_length=100, primary_key=True, serialize=False)),
                ('naam', models.CharField(max_length=100)),
                ('geometrie', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=28992)),
            ],
            options={
                'verbose_name': 'Grootstedelijkgebied',
                'verbose_name_plural': 'Grootstedelijke gebieden',
            },
        ),
        migrations.CreateModel(
            name='Ligging',
            fields=[
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('omschrijving', models.CharField(max_length=150, null=True)),
            ],
            options={
                'verbose_name': 'Ligging',
                'verbose_name_plural': 'Ligging',
            },
        ),
        migrations.CreateModel(
            name='Ligplaats',
            fields=[
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('document_mutatie', models.DateField(null=True)),
                ('document_nummer', models.CharField(max_length=20, null=True)),
                ('begin_geldigheid', models.DateField(null=True)),
                ('einde_geldigheid', models.DateField(null=True)),
                ('mutatie_gebruiker', models.CharField(max_length=30, null=True)),
                ('id', models.CharField(max_length=14, primary_key=True, serialize=False)),
                ('landelijk_id', models.CharField(max_length=16, null=True, unique=True)),
                ('vervallen', models.NullBooleanField(default=None)),
                ('geometrie', django.contrib.gis.db.models.fields.PolygonField(null=True, srid=28992)),
                ('_openbare_ruimte_naam', models.CharField(max_length=150, null=True)),
                ('_huisnummer', models.IntegerField(null=True)),
                ('_huisletter', models.CharField(max_length=1, null=True)),
                ('_huisnummer_toevoeging', models.CharField(max_length=4, null=True)),
                ('buurt', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                            related_name='ligplaatsen', to='bag.Buurt')),
            ],
            options={
                'verbose_name': 'Ligplaats',
                'ordering': ('_openbare_ruimte_naam', '_huisnummer', '_huisletter', '_huisnummer_toevoeging'),
                'verbose_name_plural': 'Ligplaatsen',
            },
            bases=(datasets.bag.models.AdresseerbaarObjectMixin, models.Model),
        ),
        migrations.CreateModel(
            name='LocatieIngang',
            fields=[
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('omschrijving', models.CharField(max_length=150, null=True)),
            ],
            options={
                'verbose_name': 'Locatie Ingang',
                'verbose_name_plural': 'Locaties Ingang',
            },
        ),
        migrations.CreateModel(
            name='Nummeraanduiding',
            fields=[
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('document_mutatie', models.DateField(null=True)),
                ('document_nummer', models.CharField(max_length=20, null=True)),
                ('begin_geldigheid', models.DateField(null=True)),
                ('einde_geldigheid', models.DateField(null=True)),
                ('mutatie_gebruiker', models.CharField(max_length=30, null=True)),
                ('id', models.CharField(max_length=14, primary_key=True, serialize=False)),
                ('landelijk_id', models.CharField(max_length=16, unique=True)),
                ('huisnummer', models.IntegerField()),
                ('huisletter', models.CharField(max_length=1, null=True)),
                ('huisnummer_toevoeging', models.CharField(max_length=4, null=True)),
                ('postcode', models.CharField(max_length=6, null=True)),
                ('type', models.CharField(choices=[('01', 'Verblijfsobject'), ('02', 'Standplaats'),
                                                   ('03', 'Ligplaats'), ('04', 'Overig gebouwd object'),
                                                   ('05', 'Overig terrein')],
                                          max_length=2, null=True)),
                ('adres_nummer', models.CharField(max_length=10, null=True)),
                ('vervallen', models.NullBooleanField(default=None)),
                ('hoofdadres', models.NullBooleanField(default=None)),
                ('_openbare_ruimte_naam', models.CharField(max_length=150, null=True)),
                ('ligplaats', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                                related_name='adressen', to='bag.Ligplaats')),
            ],
            options={
                'verbose_name': 'Nummeraanduiding',
                'ordering': ('_openbare_ruimte_naam', 'huisnummer', 'huisletter', 'huisnummer_toevoeging'),
                'verbose_name_plural': 'Nummeraanduidingen',
            },
        ),
        migrations.CreateModel(
            name='OpenbareRuimte',
            fields=[
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('document_mutatie', models.DateField(null=True)),
                ('document_nummer', models.CharField(max_length=20, null=True)),
                ('begin_geldigheid', models.DateField(null=True)),
                ('einde_geldigheid', models.DateField(null=True)),
                ('mutatie_gebruiker', models.CharField(max_length=30, null=True)),
                ('id', models.CharField(max_length=14, primary_key=True, serialize=False)),
                ('landelijk_id', models.CharField(max_length=16, null=True, unique=True)),
                ('type', models.CharField(choices=[('01', 'Weg'), ('02', 'Water'), ('03', 'Spoorbaan'),
                                                   ('04', 'Terrein'), ('05', 'Kunstwerk'),
                                                   ('06', 'Landschappelijk gebied'),
                                                   ('07', 'Administratief gebied')],
                                          max_length=2, null=True)),
                ('naam', models.CharField(max_length=150)),
                ('code', models.CharField(max_length=5, unique=True)),
                ('straat_nummer', models.CharField(max_length=10, null=True)),
                ('naam_nen', models.CharField(max_length=24)),
                ('naam_ptt', models.CharField(max_length=17)),
                ('vervallen', models.NullBooleanField(default=None)),
                ('geometrie', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=28992)),
            ],
            options={
                'verbose_name': 'Openbare Ruimte',
                'ordering': ('naam', 'id'),
                'verbose_name_plural': 'Openbare Ruimtes',
            },
        ),
        migrations.CreateModel(
            name='Pand',
            fields=[
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('document_mutatie', models.DateField(null=True)),
                ('document_nummer', models.CharField(max_length=20, null=True)),
                ('begin_geldigheid', models.DateField(null=True)),
                ('einde_geldigheid', models.DateField(null=True)),
                ('mutatie_gebruiker', models.CharField(max_length=30, null=True)),
                ('id', models.CharField(max_length=14, primary_key=True, serialize=False)),
                ('landelijk_id', models.CharField(max_length=16, unique=True)),
                ('bouwjaar', models.PositiveIntegerField(null=True)),
                ('laagste_bouwlaag', models.IntegerField(null=True)),
                ('hoogste_bouwlaag', models.IntegerField(null=True)),
                ('pandnummer', models.CharField(max_length=10, null=True)),
                ('vervallen', models.NullBooleanField(default=None)),
                ('geometrie', django.contrib.gis.db.models.fields.PolygonField(null=True, srid=28992)),
                ('bouwblok', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                               related_name='panden', to='bag.Bouwblok')),
            ],
            options={
                'verbose_name': 'Pand',
                'verbose_name_plural': 'Panden',
            },
        ),
        migrations.CreateModel(
            name='RedenAfvoer',
            fields=[
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('omschrijving', models.CharField(max_length=150, null=True)),
            ],
            options={
                'verbose_name': 'Reden Afvoer',
                'verbose_name_plural': 'Reden Afvoer',
            },
        ),
        migrations.CreateModel(
            name='RedenOpvoer',
            fields=[
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('omschrijving', models.CharField(max_length=150, null=True)),
            ],
            options={
                'verbose_name': 'Reden Opvoer',
                'verbose_name_plural': 'Reden Opvoer',
            },
        ),
        migrations.CreateModel(
            name='Stadsdeel',
            fields=[
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('begin_geldigheid', models.DateField(null=True)),
                ('einde_geldigheid', models.DateField(null=True)),
                ('geometrie', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=28992)),
                ('id', models.CharField(max_length=14, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=3, unique=True)),
                ('naam', models.CharField(max_length=40)),
                ('vervallen', models.NullBooleanField(default=None)),
                ('ingang_cyclus', models.DateField(null=True)),
                ('brondocument_naam', models.CharField(max_length=100, null=True)),
                ('brondocument_datum', models.DateField(null=True)),
                ('gemeente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                               related_name='stadsdelen', to='bag.Gemeente')),
            ],
            options={
                'verbose_name': 'Stadsdeel',
                'verbose_name_plural': 'Stadsdelen',
            },
        ),
        migrations.CreateModel(
            name='Standplaats',
            fields=[
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('document_mutatie', models.DateField(null=True)),
                ('document_nummer', models.CharField(max_length=20, null=True)),
                ('begin_geldigheid', models.DateField(null=True)),
                ('einde_geldigheid', models.DateField(null=True)),
                ('mutatie_gebruiker', models.CharField(max_length=30, null=True)),
                ('id', models.CharField(max_length=14, primary_key=True, serialize=False)),
                ('landelijk_id', models.CharField(max_length=16, null=True, unique=True)),
                ('vervallen', models.NullBooleanField(default=None)),
                ('geometrie', django.contrib.gis.db.models.fields.PolygonField(null=True, srid=28992)),
                ('_openbare_ruimte_naam', models.CharField(max_length=150, null=True)),
                ('_huisnummer', models.IntegerField(null=True)),
                ('_huisletter', models.CharField(max_length=1, null=True)),
                ('_huisnummer_toevoeging', models.CharField(max_length=4, null=True)),
                ('buurt', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                            related_name='standplaatsen', to='bag.Buurt')),
            ],
            options={
                'verbose_name': 'Standplaats',
                'ordering': ('_openbare_ruimte_naam', '_huisnummer', '_huisletter', '_huisnummer_toevoeging'),
                'verbose_name_plural': 'Standplaatsen',
            },
            bases=(datasets.bag.models.AdresseerbaarObjectMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('omschrijving', models.CharField(max_length=150, null=True)),
            ],
            options={
                'verbose_name': 'Status',
                'managed': True,
                'verbose_name_plural': 'Status',
            },
        ),
        migrations.CreateModel(
            name='Toegang',
            fields=[
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('omschrijving', models.CharField(max_length=150, null=True)),
            ],
            options={
                'verbose_name': 'Toegang',
                'verbose_name_plural': 'Toegang',
            },
        ),
        migrations.CreateModel(
            name='Unesco',
            fields=[
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('id', models.SlugField(max_length=100, primary_key=True, serialize=False)),
                ('naam', models.CharField(max_length=100)),
                ('geometrie', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=28992)),
            ],
            options={
                'verbose_name': 'Unesco',
                'verbose_name_plural': 'Unesco',
            },
        ),
        migrations.CreateModel(
            name='Verblijfsobject',
            fields=[
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('document_mutatie', models.DateField(null=True)),
                ('document_nummer', models.CharField(max_length=20, null=True)),
                ('begin_geldigheid', models.DateField(null=True)),
                ('einde_geldigheid', models.DateField(null=True)),
                ('mutatie_gebruiker', models.CharField(max_length=30, null=True)),
                ('id', models.CharField(max_length=14, primary_key=True, serialize=False)),
                ('landelijk_id', models.CharField(max_length=16, unique=True)),
                ('gebruiksdoel_code', models.CharField(max_length=4, null=True)),
                ('gebruiksdoel_omschrijving', models.CharField(max_length=150, null=True)),
                ('oppervlakte', models.PositiveIntegerField(null=True)),
                ('bouwlaag_toegang', models.IntegerField(null=True)),
                ('status_coordinaat_code', models.CharField(max_length=3, null=True)),
                ('status_coordinaat_omschrijving', models.CharField(max_length=150, null=True)),
                ('verhuurbare_eenheden', models.PositiveIntegerField(null=True)),
                ('bouwlagen', models.PositiveIntegerField(null=True)),
                ('type_woonobject_code', models.CharField(max_length=2, null=True)),
                ('type_woonobject_omschrijving', models.CharField(max_length=150, null=True)),
                ('woningvoorraad', models.NullBooleanField(default=None)),
                ('aantal_kamers', models.PositiveIntegerField(null=True)),
                ('vervallen', models.PositiveIntegerField(default=False)),
                ('geometrie', django.contrib.gis.db.models.fields.PointField(null=True, srid=28992)),
                ('_openbare_ruimte_naam', models.CharField(max_length=150, null=True)),
                ('_huisnummer', models.IntegerField(null=True)),
                ('_huisletter', models.CharField(max_length=1, null=True)),
                ('_huisnummer_toevoeging', models.CharField(max_length=4, null=True)),
                ('buurt', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                            related_name='verblijfsobjecten', to='bag.Buurt')),
                ('eigendomsverhouding', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                                          to='bag.Eigendomsverhouding')),
                ('financieringswijze', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                                         to='bag.Financieringswijze')),
                ('gebruik', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                              to='bag.Gebruik')),
                ('ligging', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                              to='bag.Ligging')),
                ('locatie_ingang', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                                     to='bag.LocatieIngang')),
            ],
            options={
                'verbose_name': 'Verblijfsobject',
                'ordering': ('_openbare_ruimte_naam', '_huisnummer', '_huisletter', '_huisnummer_toevoeging'),
                'verbose_name_plural': 'Verblijfsobjecten',
            },
            bases=(datasets.bag.models.AdresseerbaarObjectMixin, models.Model),
        ),
        migrations.CreateModel(
            name='VerblijfsobjectPandRelatie',
            fields=[
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('id', models.CharField(max_length=29, primary_key=True, serialize=False)),
                ('pand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bag.Pand')),
                ('verblijfsobject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                                      to='bag.Verblijfsobject')),
            ],
            options={
                'verbose_name': 'Verblijfsobject-Pand relatie',
                'verbose_name_plural': 'Verblijfsobject-Pand relaties',
            },
        ),
        migrations.CreateModel(
            name='Woonplaats',
            fields=[
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('document_mutatie', models.DateField(null=True)),
                ('document_nummer', models.CharField(max_length=20, null=True)),
                ('begin_geldigheid', models.DateField(null=True)),
                ('einde_geldigheid', models.DateField(null=True)),
                ('mutatie_gebruiker', models.CharField(max_length=30, null=True)),
                ('id', models.CharField(max_length=14, primary_key=True, serialize=False)),
                ('landelijk_id', models.CharField(max_length=4, unique=True)),
                ('naam', models.CharField(max_length=80)),
                ('naam_ptt', models.CharField(max_length=18, null=True)),
                ('vervallen', models.NullBooleanField(default=None)),
                ('gemeente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                               related_name='woonplaatsen', to='bag.Gemeente')),
            ],
            options={
                'verbose_name': 'Woonplaats',
                'verbose_name_plural': 'Woonplaatsen',
            },
        ),
        migrations.AddField(
            model_name='verblijfsobject',
            name='panden',
            field=models.ManyToManyField(related_name='verblijfsobjecten',
                                         through='bag.VerblijfsobjectPandRelatie', to='bag.Pand'),
        ),
        migrations.AddField(
            model_name='verblijfsobject',
            name='reden_afvoer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bag.RedenAfvoer'),
        ),
        migrations.AddField(
            model_name='verblijfsobject',
            name='reden_opvoer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bag.RedenOpvoer'),
        ),
        migrations.AddField(
            model_name='verblijfsobject',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bag.Status'),
        ),
        migrations.AddField(
            model_name='verblijfsobject',
            name='toegang',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bag.Toegang'),
        ),
        migrations.AddField(
            model_name='standplaats',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bag.Status'),
        ),
        migrations.AddField(
            model_name='pand',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bag.Status'),
        ),
        migrations.AddField(
            model_name='openbareruimte',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bag.Status'),
        ),
        migrations.AddField(
            model_name='openbareruimte',
            name='woonplaats',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    related_name='openbare_ruimtes', to='bag.Woonplaats'),
        ),
        migrations.AddField(
            model_name='nummeraanduiding',
            name='openbare_ruimte',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    related_name='adressen', to='bag.OpenbareRuimte'),
        ),
        migrations.AddField(
            model_name='nummeraanduiding',
            name='standplaats',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='adressen', to='bag.Standplaats'),
        ),
        migrations.AddField(
            model_name='nummeraanduiding',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bag.Status'),
        ),
        migrations.AddField(
            model_name='nummeraanduiding',
            name='verblijfsobject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='adressen', to='bag.Verblijfsobject'),
        ),
        migrations.AddField(
            model_name='ligplaats',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bag.Status'),
        ),
        migrations.AddField(
            model_name='gebiedsgerichtwerken',
            name='stadsdeel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    related_name='gebiedsgerichtwerken', to='bag.Stadsdeel'),
        ),
        migrations.AddField(
            model_name='buurtcombinatie',
            name='stadsdeel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='buurtcombinaties', to='bag.Stadsdeel'),
        ),
        migrations.AddField(
            model_name='buurt',
            name='buurtcombinatie',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='buurten', to='bag.Buurtcombinatie'),
        ),
        migrations.AddField(
            model_name='buurt',
            name='stadsdeel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    related_name='buurten', to='bag.Stadsdeel'),
        ),
        migrations.AddField(
            model_name='bouwblok',
            name='buurt',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='bouwblokken', to='bag.Buurt'),
        ),
        migrations.AlterIndexTogether(
            name='verblijfsobject',
            index_together={('_openbare_ruimte_naam', '_huisnummer', '_huisletter', '_huisnummer_toevoeging')},
        ),
        migrations.AlterIndexTogether(
            name='standplaats',
            index_together={('_openbare_ruimte_naam', '_huisnummer', '_huisletter', '_huisnummer_toevoeging')},
        ),
        migrations.AlterIndexTogether(
            name='nummeraanduiding',
            index_together={('_openbare_ruimte_naam', 'huisnummer', 'huisletter', 'huisnummer_toevoeging')},
        ),
        migrations.AlterIndexTogether(
            name='ligplaats',
            index_together={('_openbare_ruimte_naam', '_huisnummer', '_huisletter', '_huisnummer_toevoeging')},
        ),
    ]
