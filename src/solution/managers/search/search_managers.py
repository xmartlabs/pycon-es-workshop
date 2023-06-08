from elasticsearch_dsl import Search, Q
from typing import Dict, List, Tuple

from ..embeddings.embedding_manager import EmbeddingsManager, EmbeddingTypes
from ..es.es_manager import ESManager


class SearchManager:

    def _get_traditional_search_task_2(self, query: str, em: ESManager) -> Search:
        search = Search(using=em.es_client, index=em.index_name)
        multi_match_query = Q(
            'multi_match',
            query=query,
            fields=['title', 'overview']
        )
        filter_by_genre = Q(
            'match',
            genres='Adventure'
        )
        search = search.query("bool", must=[multi_match_query, filter_by_genre])
        return search
    
    def _get_knn_search(self, query: str, emb_type: EmbeddingTypes, k: int = 10,
                    num_candidates: int = 75) -> Dict:
        em = EmbeddingsManager()
        query_vector = em.get_embeddings_for_text(query, emb_type)
        embedding_field = ''
        if emb_type == EmbeddingTypes.ASYMMETRIC:
            embedding_field = 'sbert_asymmetric_overview_embedding'
        elif emb_type == EmbeddingTypes.SYMMETRIC:
            embedding_field = 'sbert_symmetric_overview_embedding'
        return {
            "knn": {
                "field": embedding_field,
                "query_vector": query_vector,
                "k": k,
                "num_candidates": num_candidates
            }
        }

    def execute_knn_search(self, query: str, em: ESManager, emb_type: EmbeddingTypes,
                           k: int = 10, num_candidates: int = 75, size: int = 20) -> Tuple[List[Dict], Dict]:
        knn_query = self._get_knn_search(query, emb_type, k, num_candidates)
        knn_query['size'] = size
        response = em.es_client.search(index=em.index_name, body=knn_query)
        return [self._serialize_es_results(r) for r in response['hits']['hits']], knn_query


    
    def execute_hybrid_search(self, query: str, em: ESManager, emb_type: EmbeddingTypes,
                              knn_k: int = 10, knn_num_candidates: int = 75,
                              size: int = 20) -> Tuple[List[Dict], Dict]:
        # Create KKN search query
        knn_query = self._get_knn_search(query, emb_type, knn_k, knn_num_candidates)
        # Create traditional search query
        traditional_query = self._get_traditional_search(query, em).to_dict()
        # Create hybrid search query
        hybrid_query = {
            'query': traditional_query['query'],
            'knn': knn_query['knn'],
            'size': size
        }
        response = em.es_client.search(index=em.index_name, body=hybrid_query)
        return [self._serialize_es_results(r) for r in response['hits']['hits']], hybrid_query
