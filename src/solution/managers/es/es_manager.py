import os

from elasticsearch_dsl import DenseVector, Document, Text, Keyword, MetaField


ES_DENSE_VECTOR_M_VALUE = os.environ.get('ES_DENSE_VECTOR_M_VALUE', 16)
ES_DENSE_VECTOE_EF_CONSTRUCTION_VALUE = os.environ.get('ES_DENSE_VECTOE_EF_CONSTRUCTION_VALUE', 50)


class ESManager:

    def get_document_definition_solution_task_1(self, text_analyzer=None) -> Document:
        if not text_analyzer:
            text_analyzer = self._get_default_analyzer()

        class MovieDoc(Document):
            id = Keyword()
            title = Text(analyzer=text_analyzer)
            genres = Keyword(multi=True)
            director = Keyword()
            protagonists = Keyword(multi=True)
            overview = Text(analyzer=text_analyzer)

            class Meta:
                dynamic = MetaField('false')

        return MovieDoc
    
    def get_document_definition_solution_task_3(self, text_analyzer=None) -> Document:
        if not text_analyzer:
            text_analyzer = self._get_default_analyzer()

        class MovieDoc(Document):
            id = Keyword()
            title = Text(analyzer=text_analyzer)
            genres = Keyword(multi=True)
            director = Keyword(multi=True)
            protagonists = Keyword()
            overview = Text(analyzer=text_analyzer)
            sbert_symmetric_overview_embedding = DenseVector(
                dims=768, index=True, similarity='cosine',
                index_options={
                    'type': 'hnsw',
                    'm': ES_DENSE_VECTOR_M_VALUE,
                    'ef_construction': ES_DENSE_VECTOE_EF_CONSTRUCTION_VALUE
                }
            )
            sbert_asymmetric_overview_embedding = DenseVector(
                dims=768, index=True, similarity='dot_product',
                index_options={
                    'type': 'hnsw',
                    'm': ES_DENSE_VECTOR_M_VALUE,
                    'ef_construction': ES_DENSE_VECTOE_EF_CONSTRUCTION_VALUE
                }
            )

            class Meta:
                dynamic = MetaField('false')

        return MovieDoc