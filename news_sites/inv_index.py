import xml.etree.ElementTree as ET
import preprocessing
import os

#Input: data read in json format and a file name in which the xml file will be saved.
#Output: Does not return anything, but creates an xml file with name 'filename' that contains the inverted index
#Functionality: Builds up the inverted index in xml format.
def generate_inverted_index(data, filename):
    if not os.path.exists(filename):

        unique_stemmed_data = preprocessing.get_unique_lemmas(data=data)
        tf_idf_data = preprocessing.tf_idf(data)
        data_xml = ET.Element('inverted_index')

        for i in range(len(unique_stemmed_data)):
            lemma = ET.SubElement(data_xml, 'lemma')
            lemma.set('name', unique_stemmed_data[i])

            for j in range(len(data)):
                document = ET.SubElement(lemma, 'document')
                document.set('id', data[j]['url'])
                document.set('weight', str(tf_idf_data[i][j]))

        b_xml = ET.tostring(data_xml)

        with open(filename,'wb') as f:
            f.write(b_xml)
    else:print('Function generate_inverted_index could not generate xml file because the file already exists.')

#Input:file which is the name of the xml file that we want to load
#Output: The inverted index 
def load_inverted_index(file):
    with open(file, 'r') as f:
        data = f.read()
    return data