import logging
import os
import pandas as pd

from typing import Dict

from ..embeddings.embedding_manager import EmbeddingTypes


class DatasetManager:

    def _map_movie_into_es_solution_task_1(self, movie: Dict) -> Dict:
        return {
            'id': movie['item_id'],
            'title': movie['title'],
            'genres': [g for g in movie['genres']],
            'director': movie['director'],
            'protagonist': [p for p in movie['protagonist']],
            'overview': movie['overview']
        }


    def _map_movie_into_es_solution_task_3(self, movie: Dict) -> Dict:
        return {
            'id': movie['item_id'],
            'title': movie['title'],
            'genres': [g for g in movie['genres']],
            'director': movie['director'],
            'protagonist': [p for p in movie['protagonist']],
            'overview': movie['overview'],
            'sbert_symmetric_overview_embedding': self._get_embedding_for_movie(
                movie, EmbeddingTypes.SYMMETRIC),
            'sbert_asymmetric_overview_embedding': self._get_embedding_for_movie(
                movie, EmbeddingTypes.ASYMMETRIC)
        }
