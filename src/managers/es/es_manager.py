import os

from elasticsearch import Elasticsearch
from elasticsearch_dsl import analyzer, DenseVector, Document, Index, \
    Text, Keyword, token_filter, MetaField, Search


ES_DENSE_VECTOR_M_VALUE = os.environ.get('ES_DENSE_VECTOR_M_VALUE', 16)
ES_DENSE_VECTOE_EF_CONSTRUCTION_VALUE = os.environ.get('ES_DENSE_VECTOE_EF_CONSTRUCTION_VALUE', 50)


class ESManager:

    def __init__(self, index_name: str = None):
        self.index_name = index_name or os.environ.get('INDEX_NAME', 'test')
        elasticsearch_host = os.environ.get('ELASTIC_HOST', 'http://elasticsearch:9200/')
        elasticsearch_user = os.environ.get('ELASTIC_USER')
        elasticsearch_password = os.environ.get('ELASTIC_PASSWORD')
        if not elasticsearch_user:
            self.es_client = Elasticsearch(elasticsearch_host)
        else:
            self.es_client = Elasticsearch(
                elasticsearch_host, http_auth=(elasticsearch_user, elasticsearch_password)
            )

    def _get_index_definition(self, index_name: str) -> Index:
        index = Index(index_name)
        index.settings(
            number_of_shards=1,
            number_of_replicas=0
        )
        return index

    def _get_default_analyzer(self) -> analyzer:
        english_stopwords = token_filter("english_stopwords", "stop", stopwords="_english_")
        english_stemmer = token_filter("english_stemmer", "stemmer", language="english")
        english_possessive_stemmer = token_filter(
            "english_possessive_stemmer",
            "stemmer",
            language="possessive_english"
        )
        default_analyzer = analyzer(
            "default_analyzer",
            tokenizer="whitespace",
            filter=[
                english_possessive_stemmer,
                "lowercase",
                english_stopwords,
                english_stemmer
            ],
            char_filter=["html_strip"]
        )
        return default_analyzer

    def get_document_definition(self, text_analyzer=None) -> Document:
        if not text_analyzer:
            text_analyzer = self._get_default_analyzer()

        class MovieDoc(Document):
            id = Keyword()
            title = Text(analyzer=text_analyzer)

            class Meta:
                dynamic = MetaField('false')

        return MovieDoc

    def _create_index(self, index_name: str):
        index = self._get_index_definition(index_name)
        document = self.get_document_definition()
        index.document(document)
        index.create(using=self.es_client)

    def _drop_index_if_exists(self, index_name: str) -> bool:
        if self.es_client.indices.exists(index=index_name):
            self.es_client.indices.delete(index=index_name, ignore=[400, 404])

    def create_index(self, drop_index_if_exists: bool = False):
        if self.es_client.indices.exists(index=self.index_name):
            if drop_index_if_exists:
                self.es_client.indices.delete(index=self.index_name, ignore=[400, 404])
            else:
                return
        self._create_index(self.index_name)

    def save_document(self, document_dict: dict):
        document = self.get_document_definition()()
        for key in document_dict:
            document[key] = document_dict[key]
        document.save(index=self.index_name, using=self.es_client)
