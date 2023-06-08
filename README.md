# Workshop: Create a Powerful Movie Search Tool in Python with Elasticsearch 8 and Semantic Embeddings

## Workshop Details:

Discover the art of building a robust movie search system in Python as we dive into the captivating world of Elasticsearch 8.

Gain hands-on expertise in harnessing Elasticsearch’s powerful search tools to unlock unparalleled results. Elevate your search capabilities by seamlessly integrating semantic vectors into Elasticsearch indices, revolutionizing how users find their favorite items. Moreover, master the implementation of these cutting-edge concepts in Python projects using the elasticsearch-dsl package.

The workshop will explore:
- Different field types and available queries for traditional search implementation in Elasticsearch
- Defining and creating indices in Elasticsearch from a Python project
- Examples of creating and executing queries in Python
- What are semantic vectors and how can we use them
- Including semantic vectors in Elasticsearch using dense_vectors and KNN queries
- Implementing vector-based searches using KNN in Elasticsearch from Python
- Developing a Python search system that combines traditional and KNN search (Hybrid Search) on a dataset.

## Workshop requirements

To participate on this workshop, the only two requirements you need are having [docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/) installed in your machine. You can install both tools following the provided links.

- [docker](https://docs.docker.com/engine/install/)
- [docker-compose](https://docs.docker.com/compose/install/)

## Workshop

### Section 1: Set Up 

In this section, we will build all the containers required for the workshop and learn how to interact with them from the terminal. If you are new to Docker, don't worry, the commands we need to execute are simple.


1. Clone the repository to your machine

```bash
git clone <complete-with-the-repo>
```

2. Build the containers using `docker-compose`

```bash
docker-compose build
```

3. Interact with the backend container
```bash
# Open a bash terminal in the backend container
docker-compose run backend bash
# Open a python shell
python
# Interact with the shell :)
```

### Section 2: Dataset Understanding

In this workshop, we will be working with a movies dataset, which is available in the file movie_features.parquet. To make interaction with the dataset easier, we have provided the `DatasetManager` class with some helpful functions. Let's explore some of these functions by executing some commands.

1. Import the manager class
```python
from managers import DatasetManager
dm = DatasetManager()
```

2. Get the movies dataset and analyze some data
```python
ds = dm._get_movies_dataset()
type(ds)
len(list(ds))
first_row = next(ds)
type(first_row)
first_row
second_row = next(ds)
second_row
third_row = next(ds)
```

### Section 3: ElasticSearch Management

To facilitate interaction with ElasticSearch from Python, we have provided the ESManager class. This class allows us to create and modify indexes within the cluster. Let's explore and test some examples using this class:

1. Import the manager and initialize it with the index name `workshop-v1`.

```python
from managers import ESManager
em = ESManager('workshop-v1')
```

2. Create an index using the default implementation provided:
   
```python
em.create_index()
```

3. Verify the index was successfully created using Kibana. In your browser, navigate to http://localhost:5601 and then go to the Dev Tools section. Execute the following commands:
   
```bash
GET _cat/indices
GET workshop-v1/_mapping
```

4. Import some data into the index. We have included a function `import_movies_into_es` in the `DatasetManager` to accomplish this. Let's start by uploading only 100 movies.

```python
from managers import ESManager
from managers import DatasetManager
em = ESManager('workshop-v1')
dm = DatasetManager()
dm.import_movies_into_es(em, 100)
```

5. Verify the data was successfully imported by executing some queries in Kibana

```bash
GET workshop-v1/_search
{
  "query": {
    "match_all": {}
  },
  "size": 20
}

GET workshop-v1/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "multi_match": {
            "query": "Tom",
            "fields": [
              "title" 
            ]
          }
        }
      ]
    }
  },
  "size": 20
}
```

6. Feel free to explore and experiment with different queries and index modifications using the ESManager class.

### Section 4: Task 1: Modifying the ES index

Great! Now that we know how to use the `DatasetManager` and `ESManager` helper classes, let's modify the existing index by introducing some new fields: `genres`, `director`, `protagonists`, and `overview`. Here's how to do it:


1. To incorporate the new fields, modify the `get_document_definition` function within the `ESManager` class. Consider which field class would best suit the data structure before proceeding. If you are unsure about the appropriate field classes, don't worry—we've provided a potential solution in the `get_document_definition_solution_task_1` function inside the solution folder.

2. Once you've made the necessary modifications to the function, you can test it by creating a new index:
```python
from managers import ESManager
em = ESManager('workshop-v2')
em.create_index()
```
You can verify the index was created correctly using Kibana, just as we did before.

1. Next, let's import some data into the new index. Modify the `_map_movie_into_es` function inside the `DatasetManager` class. We have also provided a tentative solution in the solution folder :)

2. With the function modified, you can now import data into the new index:
```python
from managers import ESManager
from managers import DatasetManager
em = ESManager('workshop-v2')
dm = DatasetManager()
dm.import_movies_into_es(em, 100)
``` 

1. Now, let's query some data from the new index. Use the following queries:
```bash
GET workshop-v2/_search
{
  "query": {
    "match_all": {}
  },
  "size": 20
}

GET workshop-v1/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "multi_match": {
            "query": "Tom",
            "fields": [
              "title",
              "overview"
            ]
          }
        }
      ]
    }
  },
  "size": 20
}
```

### Section 5: ElasticSearch Queries from Python (elasticsearch-dsl)
To execute the query we used in Kibana directly from Python using the `elasticsearch-dsl` package, we can use the `SearchManager` helper class. This class allows you to construct and execute Elasticsearch queries in Python. Here's an example of how to use it:

```python
from managers import ESManager, SearchManager

em = ESManager('workshop-v2')
sm = SearchManager()

results, query = sm.execute_traditional_search("Tom", em)
for r in results:
  sm.print_result(r)

sm.print_query(query)
```

### Section 6: Task 2: Modifying the Python query

Lets modify the `execute_traditional_search` introducing a filter by `Adventure` genre.

### Section 7: Embeddings
Excellent! We have developed an outstanding product. However, what happens when queries include words that are not present in the datasets? This is where the concept of embeddings and KNN (K-Nearest Neighbors) queries in ElasticSearch come into play. To support this functionality, we have introduced a new container called `embeddings-generator`, which implements a basic embedding generation capability. In alignment with the workshop's approach, we have also created a helper class called `EmbeddingsManager` that simplifies the interaction with the container. Let's explore some examples.

Before proceeding, please uncomment the embeddings-generator section in the docker-compose file and restart all the containers.

```python
from managers import EmbeddingsManager, EmbeddingTypes
em = EmbeddingsManager()
query_vector_sym = em.get_embeddings_for_text('cats', EmbeddingTypes.SYMMETRIC)
print(query_vector_sym)
query_vector_asym = em.get_embeddings_for_text('cats', EmbeddingTypes.ASYMMETRIC)
print(query_vector_asym)
```

### Section 8: Task 3: Include the embedding inside the index and import new data

Let's enhance the instructions for modifying the existing index by introducing two new fields: `sbert_symmetric_overview_embedding` and `sbert_asymmetric_overview_embedding`.

Here are some important considerations to keep in mind:

   - The field type for both `sbert_symmetric_overview_embedding` and `sbert_asymmetric_overview_embedding` should be set to dense_vectors. This allows Elasticsearch to store dense vector representations.
  - Review the size required for the vectors.
  - Take into account that symmetric vectors tend to perform better with the `cosine distance metric`, while asymmetric vectors tend to perform better with the `dot product distance` metric. Consider these differences when selecting the appropriate distance metric for each field.

1. Modify the function `get_document_definition` for the `ESManager` class and introduce the new fields. Same as before, a possible solution exists in the function  `get_document_definition_solution_exercise_3`.

2. Once you've made the necessary modifications to the function, you can test it by creating a new index:
```python
from managers import ESManager
em = ESManager('workshop-v3')
em.create_index()
```
You can check the index was correctly created using Kibana as we did before.

3. Now, let's import some data in the index. Modify the function `_map_movie_into_es` inside the `DatasetManager` class. We have also provided a tentantive solution in the solution folder :)

4. Next, let's import some data into the new index. Modify the `_map_movie_into_es` function inside the `DatasetManager` class. We have also provided a tentative solution in the solution folder :)

5. With the function modified, you can import data into the new index:
```python
from managers import ESManager
from managers import DatasetManager
em = ESManager('workshop-v3')
dm = DatasetManager()
dm.import_movies_into_es(em, 20)
```

6. Finally, let's query some data from the new index. Use the following queries:
```bash
GET workshop-v3/_search
{
  "query": {
    "match_all": {}
  },
  "size": 20
}
```
### Section 9: Final implementation using KNN

Okay, now that we have everything set up, let's discuss how we can use these embeddings to retrieve data and perform a KNN search query. You don't need to worry about implementing it yourself, as we already have the solution for you. Simply copy the `_get_knn_search` and `execute_knn_search` functions from the solution folder and paste them inside the `ESManager` class.

Once you've completed that step, we can proceed to execute some queries using the KNN search functionality.

```python
from managers import EmbeddingsManager, EmbeddingTypes
from managers import ESManager

em = ESManager('workshop-v3')
results, query = sm.execute_knn_search('War', em, EmbeddingTypes.SYMMETRIC)
for r in results:
  sm.print_result(r)
sm.print_query(query)
```

You might wonder: wait, can I integrate both approaches? Absolutely! You can seamlessly integrate both approaches. To explore this integration, you can refer to the execute_hybrid_search function in the solution folder. This function combines the power of embeddings and traditional search techniques, enabling you to perform hybrid searches. Feel free to test it out and witness firsthand how you can leverage this functionality.

```python
from managers import EmbeddingsManager, EmbeddingTypes
from managers import ESManager

em = ESManager('workshop-v3')
results, query = sm.execute_hybrid_search('War', em, EmbeddingTypes.SYMMETRIC)
for r in results:
  sm.print_result(r)
sm.print_query(query)
```
### Conclusions and next steps

You have successfully completed the "Create a Powerful Movie Search Tool in Python with Elasticsearch 8 and Semantic" workshop. Thank you for participating! Throughout the workshop, you have learned several key topics, including:

1. Managing ES Indexes from Python
2. Implementing traditional queries from Python using the elasticsearch-dsl package
3. An introduction to semantic vectors and their role in enhancing search capabilities using knn queries
4. A workaround to use the elasticsearch-dsl package with newer versions of Elasticsearch without encountering compatibility issues

If you are interested in further expanding your knowledge in this area, here are some ideas you can explore:

1. Building more complex queries: Take the queries developed in the workshop and make them more sophisticated. Explore the various features and capabilities offered by Elasticsearch to achieve even better search results.

2. Testing different embedding models: Experiment with alternative embedding models (for example the provided by OpenAI) that may offer improved performance compared to the one used in the workshop. These models can be utilized in the latest version of Elasticsearch (8.8.0) to enhance the search experience further.

3. Deploying your model directly in Elasticsearch: Explore the possibility of deploying your own custom-trained embedding model directly within Elasticsearch. This allows you to leverage your model's unique capabilities and tailor it specifically to your search requirements.

By delving deeper into these areas, you can enhance your expertise and leverage Elasticsearch to build even more powerful and customized search applications.


## Join the Xmartlabs Community! 
At Xmartlabs we love to share our knowledge through our open source work. Feel free to check out our [GitHub profile](https://github.com/xmartlabs) and contribute in any way you see fit. You can also explore our [blog](https://blog.xmartlabs.com/), where we regularly post new insights and discoveries. See you there!

