import argparse
import json
import logging

from managers import DatasetManager, ESManager, SearchManager, EmbeddingTypes
from typing import Dict


def print_result(r: Dict) -> None:
    print('-----------------------------')
    print(f'Title: {r["title"]}')
    print(f'Overview: {r["overview"]}')
    print(f'Score: {r["score"]}')
    print('-----------------------------')


def print_query(query: Dict) -> None:
    print(json.dumps(query))


if __name__ == '__main__':
   print("Hello word")