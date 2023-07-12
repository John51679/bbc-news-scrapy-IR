import json
from nltk import pos_tag
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import math

#Input: file which is the name of the json file we want to load from directory
#output: Returns a list of data read from the json file
def load_json_file(file):
    with open(file,"r") as json_file:
        data = json.load(json_file)
    return data

#Input: data which is a list of data read from the json file
#Output: Does not return anything, but updates the json file with the input data in json format
def update_json_file(data):
    with open('news_sites/news_bbc.json','w+') as json_file:
            json_file.seek(0,2)
            json.dump(data, json_file, indent = 4)
            #json_file.truncate() 

#Input: data which is a list of data read from the json file
#Output: Returns the updated version of the input, including PoStag data
#Functionality: Create tag 'postag' in data input and at the same time update the json file with the new tag including PoStag data
def create_postags(data):
    if (data[0].get('postag')==None):

        for i in data:
            content = word_tokenize(i.get('content'))
            postag = pos_tag(content)
            i['postag'] = postag
        update_json_file(data)

    else: print("Function create_postags has identified already existing tags with name 'postag' in file.")
    return data

#Input: data which is a list of data read from the json file
#Output: Returns a boolean flag which indicates whether function stopword_removal_stemming should execute or not
#Functionality: Detects if stopwords are found within the data given as input and if so returns true, otherwise false
def check_stopwords(data):
    check_flag = False
    closed_class = ['CD', 'CC', 'DT', 'EX', 'IN', 'LS', 'MD', 'PDT', 'POS', 'PRP', 'PRP$', 'RP', 'TO', 'UH', 'WDT', 'WP', 'WP$', 'WRB']
    if (data[0].get('postag')==None):
        print("tag 'postag' is not identified anywhere inside file. Make sure you have used 'create_postags(json_file)' before using this function!")
    else:
        for i in data[0]['postag']:

            if i[1] in closed_class:
                check_flag = True
                break 
    return check_flag

#Input: data which is a list of data read from the json file and check_flag which is explained in the above function
#Output: returns the processed input data, that excludes stopwords, and all remaining words are stemmed
#Functionality: stopword removal and stemming
def stopword_removal_stemming(data,check_flag):
    ps = PorterStemmer()
    closed_class = ['CD', 'CC', 'DT', 'EX', 'IN', 'LS', 'MD', 'PDT', 'POS', 'PRP', 'PRP$', 'RP', 'TO', 'UH', 'WDT', 'WP', 'WP$', 'WRB']
    if check_flag:
        for i in data:

            open_class_tags = []

            for j in i['postag']:
                if j[1] not in closed_class:
                    open_class_tags.append([ps.stem(j[0]),j[1]])

            i['postag'] = open_class_tags
        
        update_json_file(data)
    return data

#Input:data which is a list of data from the json file
#Output:Returns a list of all unique words found within the input data
def get_unique_lemmas(data):
    unique_stemmed_data = []
    for i in data:
        for j in i['postag']:
            if j[0] not in unique_stemmed_data: unique_stemmed_data.append(j[0])
    return unique_stemmed_data

#Input: data which is a list of data from the json file
#Output: Returns calculated tf-idf metric for each unique stem found within the input data.
def tf_idf(data):
    tf_idf_data = []
    unique_stemmed_data = get_unique_lemmas(data=data)
    for i in range(len(unique_stemmed_data)):
        tf = []
        tf_idf_data.append([])
        for d in data:
            document_words = []
            for j in d['postag']:
                document_words.append(j[0])
            tf.append(document_words.count(unique_stemmed_data[i]))
        df = len(tf) - tf.count(0)
        idf = math.log10(len(tf)/df)
        for d in tf:
            tf_idf_data[i].append(d*idf)
    return tf_idf_data