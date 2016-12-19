import logging

from django.conf import settings


from . import models
from ..generic import index
from . import documents

log = logging.getLogger(__name__)

HR_DOC_TYPES = (
    documents.VestigingenMeta,
)


class DeleteHrIndexTask(index.DeleteIndexTask):
    index = settings.ELASTIC_INDICES['DS_BAG']
    doc_types = HR_DOC_TYPES


class IndexHrTask(index.ImportIndexTask):
    name = "index hr data"
    index = settings.ELASTIC_INDICES['DS_BAG']

    queryset = models.DataSelectie.objects

    def convert(self, obj):
        return documents.meta_from_hrdataselectie(obj)


class BuildIndexHrJob(object):
    name = "Create new search-index for all HR data from database"

    @staticmethod
    def tasks():
        return [IndexHrTask()]


class DeleteIndexHrJob(object):
    name = "Delete HR related indexes"

    @staticmethod
    def tasks():
        return [DeleteHrIndexTask()]
