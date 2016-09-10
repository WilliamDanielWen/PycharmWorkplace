from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import numpy as np
import pandas as pd
#documents
document = (" of that that where how a the         doc   blue  ."
            , "a the of                                                           doc yellow."
            , " a the that which of                                   doc green")
querry_set = ("blue") #  search terms


countVectorizer = CountVectorizer(stop_words ='english')
#learn the vocabulary in  document
countVectorizer.fit_transform(document)
print 'vocabulary learned in document\n',countVectorizer.vocabulary_


#produce the frequency in "vocabulary" for each product title
doc_term_fq_matrix=countVectorizer.transform(document)
print "\n doc_term_fq_matrix \n",doc_term_fq_matrix.todense()


# get idf for each vocabulary
tfidf_transformer = TfidfTransformer(norm="l2",smooth_idf=True)
tfidf_transformer.fit(doc_term_fq_matrix)
#get the idf matrix
tf_idf_matrix=tfidf_transformer.transform(doc_term_fq_matrix)


print "\n tf-idf matrix: \n",tf_idf_matrix.todense()


#count the frequency in for each query
count_vect_querry = CountVectorizer(stop_words ='english',binary=True)
count_vect_querry.fit(document)
querry_set_term_fq_matrix=count_vect_querry.transform(querry_set)
print "\n querry_set_term_fq_matrix\n",querry_set_term_fq_matrix.todense()

#tf_idf_matrix=np.transpose(tf_idf_matrix)
#print "\n tf-idf matrix transpose: \n",tf_idf_matrix.todense()
result=[]
for index in range(tf_idf_matrix.shape[0]):
    result.append((np.multiply(tf_idf_matrix[index], querry_set_term_fq_matrix[index].transpose()))[0, 0])


print "\n result: \n", np.shape(np.array(result))
pd.DataFrame({"toy-tf-idf": result}).to_csv('toy-idf.csv', index=False)