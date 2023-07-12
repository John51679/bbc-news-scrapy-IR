from bs4 import BeautifulSoup
import inv_index
import preprocessing
import time
from nltk import word_tokenize
from nltk import PorterStemmer
 
#Input: weight_list which is a list containing all tf-idf data for all content, and url_list which provides all urls that lead to that content
#Output:This function returns a list of all non-zero weight urls in descending order
#Functionality: Sort urls based on their tf-idf weights.
def sort_urls(weight_list, url_list):
    sorted_urls = []

    for i in range(len(weight_list)):
        if max(weight_list) == 0.0: break
        max_value_index = weight_list.index(max(weight_list))
        weight_list[max_value_index] = -1
        sorted_urls.append(url_list[max_value_index])
        
    return sorted_urls

#Input: weight_list whish is explained above
#Output: This function returns a list of added tf-idf weights in the case of multiple word questions.
def add_weights(weight_list):
    added_weights_list = []

    while weight_list.count([]) != 0:
        weight_list.remove([])

    if weight_list == []: return None

    for i in weight_list[0]:
        added_weights_list.append(0.0)

    for i in range(len(weight_list)):
        for j in range(len(weight_list[i])):
            added_weights_list[j] += weight_list[i][j]

    return added_weights_list
            


"""Generate part"""

start = time.time()
file = preprocessing.load_json_file('news_sites/news_bbc.json')
file = preprocessing.create_postags(file)
file = preprocessing.stopword_removal_stemming(file,preprocessing.check_stopwords(file))

filename = 'inverted_index.xml'
inv_index.generate_inverted_index(file,filename)

"""End of generate part"""


stop = time.time()
print('time taken for the creation of inverted index = ', stop - start , 'seconds')

# Reading the data inside the xml
# file to a variable under the name
# data
data = inv_index.load_inverted_index(filename)

Bs_data = BeautifulSoup(data, "xml") #parse the xml file

weight_list = []
url_list = []
correction = 0


query = [input("What are you looking for?\n")]
start = time.time()

ps = PorterStemmer()

#query = ['covid ','russia','normal','situations','news','close','salary','mental','going','memory','hey',
#        'Ukraine','war','life','good','soldier','africa','europe','america','works']

#query = ['covid russia','russia soldier','normal war','situations war','news Ukraine','close fight','salary increment','mental issues','going outside','memory loss',
#            'hey world','Ukraine russia','war now','life good','good health','soldier war','africa life','europe news','america economy','work fine']

# query = ['covid russia life','russia soldier war','normal war bad','situations war Ukraine','news Ukraine war',
#         'close fight police','salary increment work','mental issues war','going outside home','memory loss elder',
#         'hey planet earth','Ukraine russia conflict','war now situation','life good free','good health routine',
#         'soldier war health','africa life normal','europe news currently','america economy currently','work fine home',
#         'what is covid','news from covid','what about war','life is good','more about lifestyles','vaccine from breathing'
#         'more questions here','the world now','show me news','about the war']

# query = ['covid russia life now','russia soldier war ukraine','normal war bad thing','situations war Ukraine russia','news Ukraine war now',
#         'close fight police streets','salary increment work when','mental issues war impact','going outside home daily','memory loss elder news',
#         'hey good planet earth','Ukraine russia conflict news','war current situation news','life good free gold','good health routine tips',
#         'soldier war health issues','africa life normal style','europe news currently on','america food economy currently','work fine from home',
#         'what is covid 19','news from covid world','what about war ukraine','life is good here','more about culture lifestyles','vaccine from breathing air'
#         'more questions input here','the world right now','show me news here','about the war news']

for queries in query:
    query_tmp = word_tokenize(queries)
    weight_list = []
    url_list = []
    correction = 0
    #correction variable here is used to fill the url_list with all found urls only once within these for loops.
    #In case the first part of the query yields no results then correction is being added by one so that the rest of the code
    #can properly work on the next iteration and the url_list can be properly filled.

    for i in range(len(query_tmp)):
        query_tmp[i] = ps.stem(query_tmp[i])

    for lemma_index in range(len(query_tmp)):
        weight_list.append([])
        test = Bs_data.find('lemma', {'name' : query_tmp[lemma_index]})
        if test == None: 
            correction += 1
            continue
        test = test.find_all('document')
        
        for i in range(len(test)):
            weight_list[lemma_index].append(float(test[i].get('weight')))
            if lemma_index == correction:
                url_list.append(test[i].get('id'))

    weight_list = add_weights(weight_list)
    if weight_list != None:
        urls = sort_urls(weight_list,url_list)
        for i in urls:
            print(i)
    else: print("No matching results!")
end = time.time()
print('Searching time = ', (end - start)/len(query), ' seconds')