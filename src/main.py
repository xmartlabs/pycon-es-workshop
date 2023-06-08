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
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description='Elasticsearch Workshop example',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--upload-movies', action='store_true', help='upload movies')
    parser.add_argument('--create-index', action='store_true', help='create es index')
    parser.add_argument('--force-index-creation', action='store_true',
                        help='force index creation')
    parser.add_argument('--movies-limit', type=int, help='upload movies limit', required=False)
    parser.add_argument('--index-name', type=str, help='index name', required=False)
    parser.add_argument('--print-query', action='store_true', help='print-query', required=False)
  
    args = parser.parse_args()
    # Init the manager
    dm = DatasetManager()
    em = ESManager()
    sm = SearchManager()

    if args.create_index:
        em.create_index(args.force_index_creation)
    if args.upload_movies:
        dm.import_movies_into_es(args.movies_limit)

    while(True):
        user_query = input('Enter the sentence you want query or exit() to finish the program: ')
        if user_query == "exit()":
            print("Thanks for testing the movies es tool")
            break
        print(f'Executing traditional query for sentence: {user_query}')
        results, query = sm.execute_traditional_search(user_query, em)
        for r in results:
            print_result(r)
        if args.print_query:
            print_query(query)
        input("Press Enter to show knn query results...")
        results, query = sm.execute_knn_search(user_query, em, EmbeddingTypes.SYMMETRIC)
        for r in results:
            print_result(r)
        if args.print_query:
            print_query(query)
        input("Press Enter to show hybrid query results...")
        results, query = sm.execute_knn_search(user_query, em, EmbeddingTypes.SYMMETRIC)
        for r in results:
            print_result(r)
        if args.print_query:
            print_query(query)
