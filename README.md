# BBC news site crawler for Information Retrieval (IR)
This project was created as part of "Language Technology" subject in Computer Engineering & Informatics Department (CEID) of University of Patras. We created a crawler to fetch news content from a news site and after preproccesing it, store it into an inverted index file (xml file).

The inverted index, is then used in the process of information retrieval for query answering.

The project was created in `Python`. For the news site, BBC world news was chosen.
The codes that are written are

- `news_sites/news_sites/spiders/spider.py`: The crawler provided by the scrapy framework, to fetch and store content from the BBC news site, inside a json file
- `news_sites/inv_index.py`: Used for the creation/loading of the inverted index, written as an xml file
- `news_sites/preprocessing.py`: Contains all necessary functions for preproccesing, including the calculation of the tf-idf score. The language processing occurs with the help of the NLTK library.
- `news_sites/retrieval.py`: The main program of the project. It creates/loads the inverted index file, loads the json file containing all the news content gathered by scrapy's spider and answers a given query by returning the most relevant news in descending order according to relevance.
