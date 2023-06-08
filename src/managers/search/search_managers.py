import json

from elasticsearch_dsl import Search, Q
from elasticsearch_dsl.response.hit import Hit
from typing import Dict, List, Tuple, Union

from ..embeddings.embedding_manager import EmbeddingsManager, EmbeddingTypes
from ..es.es_manager import ESManager


class SearchManager:

    def _serialize_es_results(self, es_result: Union[Hit, dict]) -> Dict:
        if type(es_result) == Hit:
            return {
                'title': es_result['title'],
                'id': es_result['id'],
                'score': es_result.meta.score,
                'overview': es_result['overview'],
            }
        elif type(es_result) == dict:
            return {
                'title': es_result['_source']['title'],
                'id': es_result['_source']['id'],
                'score': es_result['_score'],
                'overview': es_result['_source']['overview'],
            }
        else:
            raise NotImplementedError

    def _get_traditional_search(self, query: str, em: ESManager) -> Search:
        search = Search(using=em.es_client, index=em.index_name)
        multi_match_query = Q(
            'multi_match',
            query=query,
            fields=['title', 'overview']
        )
        search = search.query("bool", must=[multi_match_query])
        return search

    def execute_traditional_search(self, query: str, em: ESManager, size: int = 20) -> Tuple[List[Dict], Dict]:
        traditional_search = self._get_traditional_search(query, em)
        traditional_search = traditional_search.update_from_dict({'size': size})
        results = traditional_search.execute()
        return [self._serialize_es_results(r) for r in results], traditional_search.to_dict()

    def print_result(self, r: Dict) -> None:
        print('-----------------------------')
        print(f'Title: {r["title"]}')
        print(f'Overview: {r["overview"]}')
        print(f'Score: {r["score"]}')
        print('-----------------------------')

    def print_query(self, query: Dict) -> None:
        print(json.dumps(query))
