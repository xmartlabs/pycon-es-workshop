import logging
import os
import pandas as pd

from typing import Dict, Iterable, List

from ..embeddings.embedding_manager import EmbeddingsManager, EmbeddingTypes
from ..es.es_manager import ESManager


class DatasetManager:

    def __init__(self):
        self.movies_dataset_path = os.environ.get(
            'MOVIES_PATH', './movie_features.parquet'
        )

    def _get_movies_dataset(self) -> Iterable[Dict]:
        movies_features_df = pd.read_parquet('./movie_features.parquet')
        for _, row in movies_features_df.iterrows():
            yield row

    def _get_embedding_for_movie(self, movie: Dict, emb_type: EmbeddingTypes) -> List[float]:
        em = EmbeddingsManager()
        return em.get_embeddings_for_text(movie['overview'], emb_type)

    def _map_movie_into_es(self, movie: Dict) -> Dict:
        return {
            'id': movie['item_id'],
            'title': movie['title']
        }

    def import_movies_into_es(self, es_manager: ESManager, limit: int = None) -> None:
        logging.info(f'Upload {limit if limit else "all"} movies into Elasticsearch')
        i = 0
        for movie in self._get_movies_dataset():
            if limit and i == limit:
                break
            movie_es = self._map_movie_into_es(movie)
            es_manager.save_document(movie_es)
            i += 1
        logging.info('Movies uploaded into Elasticsearch successfully')
