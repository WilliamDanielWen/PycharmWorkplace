import pandas as pd
import utils
from sklearn.ensemble import RandomForestRegressor, BaggingRegressor
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_regression

# read the data that we need from the original file
trainSet = pd.read_csv('IOFolder\subTrainSet-pv13.csv', encoding="ISO-8859-1")
testSet = pd.read_csv('IOFolder\developmentSet-pv13.csv', encoding="ISO-8859-1")

# drop features not used
trainSet = trainSet.drop(['product_uid', 'search_term'], axis=1)
testSet = testSet.drop(['product_uid', 'search_term'], axis=1)

#feature selection


#keep  all features  rmse=0.494565082773

# keep  "p_tit_tfidf","p_desc_tfidf"  "nword_query"
# rmse: 0.503337780163
#trainSet = trainSet.drop(["p_bullet_tfidf","p_brand_tfidf","p_other_tfidf","nchar_query","nchar_tit","nchar_desc","nchar_bull","nchar_bran","nchar_other","nword_tit","nword_desc","nword_bull","nword_bran","nword_other","svd_tit.1","svd_tit.2","svd_tit.3","svd_tit.4","svd_tit.5","svd_tit.6","svd_tit.7","svd_tit.8","svd_tit.9","svd_tit.10","svd_tit.11","svd_tit.12","svd_tit.13","svd_tit.14","svd_tit.15","svd_tit.16","svd_tit.17","svd_tit.18","svd_tit.19","svd_tit.20","svd_tit.21","svd_tit.22","svd_tit.23","svd_tit.24","svd_tit.25","svd_tit.26","svd_tit.27","svd_tit.28","svd_tit.29","svd_tit.30","svd_tit.31","svd_tit.32","svd_tit.33","svd_tit.34","svd_tit.35","svd_tit.36","svd_tit.37","svd_tit.38","svd_tit.39","svd_tit.40","svd_tit.41","svd_tit.42","svd_tit.43","svd_tit.44","svd_tit.45","svd_tit.46","svd_tit.47","svd_tit.48","svd_tit.49","svd_tit.50","svd_dec.1","svd_dec.2","svd_dec.3","svd_dec.4","svd_dec.5","svd_dec.6","svd_dec.7","svd_dec.8","svd_dec.9","svd_dec.10","svd_dec.11","svd_dec.12","svd_dec.13","svd_dec.14","svd_dec.15","svd_dec.16","svd_dec.17","svd_dec.18","svd_dec.19","svd_dec.20","svd_dec.21","svd_dec.22","svd_dec.23","svd_dec.24","svd_dec.25","svd_dec.26","svd_dec.27","svd_dec.28","svd_dec.29","svd_dec.30","svd_dec.31","svd_dec.32","svd_dec.33","svd_dec.34","svd_dec.35","svd_dec.36","svd_dec.37","svd_dec.38","svd_dec.39","svd_dec.40","svd_dec.41","svd_dec.42","svd_dec.43","svd_dec.44","svd_dec.45","svd_dec.46","svd_dec.47","svd_dec.48","svd_dec.49","svd_dec.50","svd_bull.1","svd_bull.2","svd_bull.3","svd_bull.4","svd_bull.5","svd_bull.6","svd_bull.7","svd_bull.8","svd_bull.9","svd_bull.10","svd_bull.11","svd_bull.12","svd_bull.13","svd_bull.14","svd_bull.15","svd_bull.16","svd_bull.17","svd_bull.18","svd_bull.19","svd_bull.20","svd_bull.21","svd_bull.22","svd_bull.23","svd_bull.24","svd_bull.25","svd_bull.26","svd_bull.27","svd_bull.28","svd_bull.29","svd_bull.30","svd_bull.31","svd_bull.32","svd_bull.33","svd_bull.34","svd_bull.35","svd_bull.36","svd_bull.37","svd_bull.38","svd_bull.39","svd_bull.40","svd_bull.41","svd_bull.42","svd_bull.43","svd_bull.44","svd_bull.45","svd_bull.46","svd_bull.47","svd_bull.48","svd_bull.49","svd_bull.50","svd_bran.1","svd_bran.2","svd_bran.3","svd_bran.4","svd_bran.5","svd_bran.6","svd_bran.7","svd_bran.8","svd_bran.9","svd_bran.10","svd_bran.11","svd_bran.12","svd_bran.13","svd_bran.14","svd_bran.15","svd_bran.16","svd_bran.17","svd_bran.18","svd_bran.19","svd_bran.20","svd_oth 1","svd_oth 2","svd_oth 3","svd_oth 4","svd_oth 5","svd_oth 6","svd_oth 7","svd_oth 8","svd_oth 9","svd_oth 10","svd_oth 11","svd_oth 12","svd_oth 13","svd_oth 14","svd_oth 15","svd_oth 16","svd_oth 17","svd_oth 18","svd_oth 19","svd_oth 20","svd_oth 21","svd_oth 22","svd_oth 23","svd_oth 24","svd_oth 25","svd_oth 26","svd_oth 27","svd_oth 28","svd_oth 29","svd_oth 30","svd_oth 31","svd_oth 32","svd_oth 33","svd_oth 34","svd_oth 35","svd_oth 36","svd_oth 37","svd_oth 38","svd_oth 39","svd_oth 40","svd_oth 41","svd_oth 42","svd_oth 43","svd_oth 44","svd_oth 45","svd_oth 46","svd_oth 47","svd_oth 48","svd_oth 49","svd_oth 50"],axis=1)
#testSet = testSet.drop(["p_bullet_tfidf","p_brand_tfidf","p_other_tfidf","nchar_query","nchar_tit","nchar_desc","nchar_bull","nchar_bran","nchar_other","nword_tit","nword_desc","nword_bull","nword_bran","nword_other","svd_tit.1","svd_tit.2","svd_tit.3","svd_tit.4","svd_tit.5","svd_tit.6","svd_tit.7","svd_tit.8","svd_tit.9","svd_tit.10","svd_tit.11","svd_tit.12","svd_tit.13","svd_tit.14","svd_tit.15","svd_tit.16","svd_tit.17","svd_tit.18","svd_tit.19","svd_tit.20","svd_tit.21","svd_tit.22","svd_tit.23","svd_tit.24","svd_tit.25","svd_tit.26","svd_tit.27","svd_tit.28","svd_tit.29","svd_tit.30","svd_tit.31","svd_tit.32","svd_tit.33","svd_tit.34","svd_tit.35","svd_tit.36","svd_tit.37","svd_tit.38","svd_tit.39","svd_tit.40","svd_tit.41","svd_tit.42","svd_tit.43","svd_tit.44","svd_tit.45","svd_tit.46","svd_tit.47","svd_tit.48","svd_tit.49","svd_tit.50","svd_dec.1","svd_dec.2","svd_dec.3","svd_dec.4","svd_dec.5","svd_dec.6","svd_dec.7","svd_dec.8","svd_dec.9","svd_dec.10","svd_dec.11","svd_dec.12","svd_dec.13","svd_dec.14","svd_dec.15","svd_dec.16","svd_dec.17","svd_dec.18","svd_dec.19","svd_dec.20","svd_dec.21","svd_dec.22","svd_dec.23","svd_dec.24","svd_dec.25","svd_dec.26","svd_dec.27","svd_dec.28","svd_dec.29","svd_dec.30","svd_dec.31","svd_dec.32","svd_dec.33","svd_dec.34","svd_dec.35","svd_dec.36","svd_dec.37","svd_dec.38","svd_dec.39","svd_dec.40","svd_dec.41","svd_dec.42","svd_dec.43","svd_dec.44","svd_dec.45","svd_dec.46","svd_dec.47","svd_dec.48","svd_dec.49","svd_dec.50","svd_bull.1","svd_bull.2","svd_bull.3","svd_bull.4","svd_bull.5","svd_bull.6","svd_bull.7","svd_bull.8","svd_bull.9","svd_bull.10","svd_bull.11","svd_bull.12","svd_bull.13","svd_bull.14","svd_bull.15","svd_bull.16","svd_bull.17","svd_bull.18","svd_bull.19","svd_bull.20","svd_bull.21","svd_bull.22","svd_bull.23","svd_bull.24","svd_bull.25","svd_bull.26","svd_bull.27","svd_bull.28","svd_bull.29","svd_bull.30","svd_bull.31","svd_bull.32","svd_bull.33","svd_bull.34","svd_bull.35","svd_bull.36","svd_bull.37","svd_bull.38","svd_bull.39","svd_bull.40","svd_bull.41","svd_bull.42","svd_bull.43","svd_bull.44","svd_bull.45","svd_bull.46","svd_bull.47","svd_bull.48","svd_bull.49","svd_bull.50","svd_bran.1","svd_bran.2","svd_bran.3","svd_bran.4","svd_bran.5","svd_bran.6","svd_bran.7","svd_bran.8","svd_bran.9","svd_bran.10","svd_bran.11","svd_bran.12","svd_bran.13","svd_bran.14","svd_bran.15","svd_bran.16","svd_bran.17","svd_bran.18","svd_bran.19","svd_bran.20","svd_oth 1","svd_oth 2","svd_oth 3","svd_oth 4","svd_oth 5","svd_oth 6","svd_oth 7","svd_oth 8","svd_oth 9","svd_oth 10","svd_oth 11","svd_oth 12","svd_oth 13","svd_oth 14","svd_oth 15","svd_oth 16","svd_oth 17","svd_oth 18","svd_oth 19","svd_oth 20","svd_oth 21","svd_oth 22","svd_oth 23","svd_oth 24","svd_oth 25","svd_oth 26","svd_oth 27","svd_oth 28","svd_oth 29","svd_oth 30","svd_oth 31","svd_oth 32","svd_oth 33","svd_oth 34","svd_oth 35","svd_oth 36","svd_oth 37","svd_oth 38","svd_oth 39","svd_oth 40","svd_oth 41","svd_oth 42","svd_oth 43","svd_oth 44","svd_oth 45","svd_oth 46","svd_oth 47","svd_oth 48","svd_oth 49","svd_oth 50"],axis=1)

# keep  "p_tit_tfidf","p_desc_tfidf"  "nword_query" "p_bullet_tfidf","p_brand_tfidf","p_other_tfidf"
#  rmse:  0.501151668033
#trainSet = trainSet.drop(["nchar_query","nchar_tit","nchar_desc","nchar_bull","nchar_bran","nchar_other","nword_tit","nword_desc","nword_bull","nword_bran","nword_other","svd_tit.1","svd_tit.2","svd_tit.3","svd_tit.4","svd_tit.5","svd_tit.6","svd_tit.7","svd_tit.8","svd_tit.9","svd_tit.10","svd_tit.11","svd_tit.12","svd_tit.13","svd_tit.14","svd_tit.15","svd_tit.16","svd_tit.17","svd_tit.18","svd_tit.19","svd_tit.20","svd_tit.21","svd_tit.22","svd_tit.23","svd_tit.24","svd_tit.25","svd_tit.26","svd_tit.27","svd_tit.28","svd_tit.29","svd_tit.30","svd_tit.31","svd_tit.32","svd_tit.33","svd_tit.34","svd_tit.35","svd_tit.36","svd_tit.37","svd_tit.38","svd_tit.39","svd_tit.40","svd_tit.41","svd_tit.42","svd_tit.43","svd_tit.44","svd_tit.45","svd_tit.46","svd_tit.47","svd_tit.48","svd_tit.49","svd_tit.50","svd_dec.1","svd_dec.2","svd_dec.3","svd_dec.4","svd_dec.5","svd_dec.6","svd_dec.7","svd_dec.8","svd_dec.9","svd_dec.10","svd_dec.11","svd_dec.12","svd_dec.13","svd_dec.14","svd_dec.15","svd_dec.16","svd_dec.17","svd_dec.18","svd_dec.19","svd_dec.20","svd_dec.21","svd_dec.22","svd_dec.23","svd_dec.24","svd_dec.25","svd_dec.26","svd_dec.27","svd_dec.28","svd_dec.29","svd_dec.30","svd_dec.31","svd_dec.32","svd_dec.33","svd_dec.34","svd_dec.35","svd_dec.36","svd_dec.37","svd_dec.38","svd_dec.39","svd_dec.40","svd_dec.41","svd_dec.42","svd_dec.43","svd_dec.44","svd_dec.45","svd_dec.46","svd_dec.47","svd_dec.48","svd_dec.49","svd_dec.50","svd_bull.1","svd_bull.2","svd_bull.3","svd_bull.4","svd_bull.5","svd_bull.6","svd_bull.7","svd_bull.8","svd_bull.9","svd_bull.10","svd_bull.11","svd_bull.12","svd_bull.13","svd_bull.14","svd_bull.15","svd_bull.16","svd_bull.17","svd_bull.18","svd_bull.19","svd_bull.20","svd_bull.21","svd_bull.22","svd_bull.23","svd_bull.24","svd_bull.25","svd_bull.26","svd_bull.27","svd_bull.28","svd_bull.29","svd_bull.30","svd_bull.31","svd_bull.32","svd_bull.33","svd_bull.34","svd_bull.35","svd_bull.36","svd_bull.37","svd_bull.38","svd_bull.39","svd_bull.40","svd_bull.41","svd_bull.42","svd_bull.43","svd_bull.44","svd_bull.45","svd_bull.46","svd_bull.47","svd_bull.48","svd_bull.49","svd_bull.50","svd_bran.1","svd_bran.2","svd_bran.3","svd_bran.4","svd_bran.5","svd_bran.6","svd_bran.7","svd_bran.8","svd_bran.9","svd_bran.10","svd_bran.11","svd_bran.12","svd_bran.13","svd_bran.14","svd_bran.15","svd_bran.16","svd_bran.17","svd_bran.18","svd_bran.19","svd_bran.20","svd_oth 1","svd_oth 2","svd_oth 3","svd_oth 4","svd_oth 5","svd_oth 6","svd_oth 7","svd_oth 8","svd_oth 9","svd_oth 10","svd_oth 11","svd_oth 12","svd_oth 13","svd_oth 14","svd_oth 15","svd_oth 16","svd_oth 17","svd_oth 18","svd_oth 19","svd_oth 20","svd_oth 21","svd_oth 22","svd_oth 23","svd_oth 24","svd_oth 25","svd_oth 26","svd_oth 27","svd_oth 28","svd_oth 29","svd_oth 30","svd_oth 31","svd_oth 32","svd_oth 33","svd_oth 34","svd_oth 35","svd_oth 36","svd_oth 37","svd_oth 38","svd_oth 39","svd_oth 40","svd_oth 41","svd_oth 42","svd_oth 43","svd_oth 44","svd_oth 45","svd_oth 46","svd_oth 47","svd_oth 48","svd_oth 49","svd_oth 50"],axis=1)
#testSet = testSet.drop(["nchar_query","nchar_tit","nchar_desc","nchar_bull","nchar_bran","nchar_other","nword_tit","nword_desc","nword_bull","nword_bran","nword_other","svd_tit.1","svd_tit.2","svd_tit.3","svd_tit.4","svd_tit.5","svd_tit.6","svd_tit.7","svd_tit.8","svd_tit.9","svd_tit.10","svd_tit.11","svd_tit.12","svd_tit.13","svd_tit.14","svd_tit.15","svd_tit.16","svd_tit.17","svd_tit.18","svd_tit.19","svd_tit.20","svd_tit.21","svd_tit.22","svd_tit.23","svd_tit.24","svd_tit.25","svd_tit.26","svd_tit.27","svd_tit.28","svd_tit.29","svd_tit.30","svd_tit.31","svd_tit.32","svd_tit.33","svd_tit.34","svd_tit.35","svd_tit.36","svd_tit.37","svd_tit.38","svd_tit.39","svd_tit.40","svd_tit.41","svd_tit.42","svd_tit.43","svd_tit.44","svd_tit.45","svd_tit.46","svd_tit.47","svd_tit.48","svd_tit.49","svd_tit.50","svd_dec.1","svd_dec.2","svd_dec.3","svd_dec.4","svd_dec.5","svd_dec.6","svd_dec.7","svd_dec.8","svd_dec.9","svd_dec.10","svd_dec.11","svd_dec.12","svd_dec.13","svd_dec.14","svd_dec.15","svd_dec.16","svd_dec.17","svd_dec.18","svd_dec.19","svd_dec.20","svd_dec.21","svd_dec.22","svd_dec.23","svd_dec.24","svd_dec.25","svd_dec.26","svd_dec.27","svd_dec.28","svd_dec.29","svd_dec.30","svd_dec.31","svd_dec.32","svd_dec.33","svd_dec.34","svd_dec.35","svd_dec.36","svd_dec.37","svd_dec.38","svd_dec.39","svd_dec.40","svd_dec.41","svd_dec.42","svd_dec.43","svd_dec.44","svd_dec.45","svd_dec.46","svd_dec.47","svd_dec.48","svd_dec.49","svd_dec.50","svd_bull.1","svd_bull.2","svd_bull.3","svd_bull.4","svd_bull.5","svd_bull.6","svd_bull.7","svd_bull.8","svd_bull.9","svd_bull.10","svd_bull.11","svd_bull.12","svd_bull.13","svd_bull.14","svd_bull.15","svd_bull.16","svd_bull.17","svd_bull.18","svd_bull.19","svd_bull.20","svd_bull.21","svd_bull.22","svd_bull.23","svd_bull.24","svd_bull.25","svd_bull.26","svd_bull.27","svd_bull.28","svd_bull.29","svd_bull.30","svd_bull.31","svd_bull.32","svd_bull.33","svd_bull.34","svd_bull.35","svd_bull.36","svd_bull.37","svd_bull.38","svd_bull.39","svd_bull.40","svd_bull.41","svd_bull.42","svd_bull.43","svd_bull.44","svd_bull.45","svd_bull.46","svd_bull.47","svd_bull.48","svd_bull.49","svd_bull.50","svd_bran.1","svd_bran.2","svd_bran.3","svd_bran.4","svd_bran.5","svd_bran.6","svd_bran.7","svd_bran.8","svd_bran.9","svd_bran.10","svd_bran.11","svd_bran.12","svd_bran.13","svd_bran.14","svd_bran.15","svd_bran.16","svd_bran.17","svd_bran.18","svd_bran.19","svd_bran.20","svd_oth 1","svd_oth 2","svd_oth 3","svd_oth 4","svd_oth 5","svd_oth 6","svd_oth 7","svd_oth 8","svd_oth 9","svd_oth 10","svd_oth 11","svd_oth 12","svd_oth 13","svd_oth 14","svd_oth 15","svd_oth 16","svd_oth 17","svd_oth 18","svd_oth 19","svd_oth 20","svd_oth 21","svd_oth 22","svd_oth 23","svd_oth 24","svd_oth 25","svd_oth 26","svd_oth 27","svd_oth 28","svd_oth 29","svd_oth 30","svd_oth 31","svd_oth 32","svd_oth 33","svd_oth 34","svd_oth 35","svd_oth 36","svd_oth 37","svd_oth 38","svd_oth 39","svd_oth 40","svd_oth 41","svd_oth 42","svd_oth 43","svd_oth 44","svd_oth 45","svd_oth 46","svd_oth 47","svd_oth 48","svd_oth 49","svd_oth 50"],axis=1)

# keep  "p_tit_tfidf","p_desc_tfidf"  "nword_query" "p_bullet_tfidf","p_brand_tfidf","p_other_tfidf"
#  and  "nchar_query","nchar_tit","nchar_desc","nchar_bull","nchar_bran","nchar_other","nword_tit","nword_desc","nword_bull","nword_bran","nword_other"
# rmse: 0.493481988783
#trainSet = trainSet.drop(["svd_tit.1","svd_tit.2","svd_tit.3","svd_tit.4","svd_tit.5","svd_tit.6","svd_tit.7","svd_tit.8","svd_tit.9","svd_tit.10","svd_tit.11","svd_tit.12","svd_tit.13","svd_tit.14","svd_tit.15","svd_tit.16","svd_tit.17","svd_tit.18","svd_tit.19","svd_tit.20","svd_tit.21","svd_tit.22","svd_tit.23","svd_tit.24","svd_tit.25","svd_tit.26","svd_tit.27","svd_tit.28","svd_tit.29","svd_tit.30","svd_tit.31","svd_tit.32","svd_tit.33","svd_tit.34","svd_tit.35","svd_tit.36","svd_tit.37","svd_tit.38","svd_tit.39","svd_tit.40","svd_tit.41","svd_tit.42","svd_tit.43","svd_tit.44","svd_tit.45","svd_tit.46","svd_tit.47","svd_tit.48","svd_tit.49","svd_tit.50","svd_dec.1","svd_dec.2","svd_dec.3","svd_dec.4","svd_dec.5","svd_dec.6","svd_dec.7","svd_dec.8","svd_dec.9","svd_dec.10","svd_dec.11","svd_dec.12","svd_dec.13","svd_dec.14","svd_dec.15","svd_dec.16","svd_dec.17","svd_dec.18","svd_dec.19","svd_dec.20","svd_dec.21","svd_dec.22","svd_dec.23","svd_dec.24","svd_dec.25","svd_dec.26","svd_dec.27","svd_dec.28","svd_dec.29","svd_dec.30","svd_dec.31","svd_dec.32","svd_dec.33","svd_dec.34","svd_dec.35","svd_dec.36","svd_dec.37","svd_dec.38","svd_dec.39","svd_dec.40","svd_dec.41","svd_dec.42","svd_dec.43","svd_dec.44","svd_dec.45","svd_dec.46","svd_dec.47","svd_dec.48","svd_dec.49","svd_dec.50","svd_bull.1","svd_bull.2","svd_bull.3","svd_bull.4","svd_bull.5","svd_bull.6","svd_bull.7","svd_bull.8","svd_bull.9","svd_bull.10","svd_bull.11","svd_bull.12","svd_bull.13","svd_bull.14","svd_bull.15","svd_bull.16","svd_bull.17","svd_bull.18","svd_bull.19","svd_bull.20","svd_bull.21","svd_bull.22","svd_bull.23","svd_bull.24","svd_bull.25","svd_bull.26","svd_bull.27","svd_bull.28","svd_bull.29","svd_bull.30","svd_bull.31","svd_bull.32","svd_bull.33","svd_bull.34","svd_bull.35","svd_bull.36","svd_bull.37","svd_bull.38","svd_bull.39","svd_bull.40","svd_bull.41","svd_bull.42","svd_bull.43","svd_bull.44","svd_bull.45","svd_bull.46","svd_bull.47","svd_bull.48","svd_bull.49","svd_bull.50","svd_bran.1","svd_bran.2","svd_bran.3","svd_bran.4","svd_bran.5","svd_bran.6","svd_bran.7","svd_bran.8","svd_bran.9","svd_bran.10","svd_bran.11","svd_bran.12","svd_bran.13","svd_bran.14","svd_bran.15","svd_bran.16","svd_bran.17","svd_bran.18","svd_bran.19","svd_bran.20","svd_oth 1","svd_oth 2","svd_oth 3","svd_oth 4","svd_oth 5","svd_oth 6","svd_oth 7","svd_oth 8","svd_oth 9","svd_oth 10","svd_oth 11","svd_oth 12","svd_oth 13","svd_oth 14","svd_oth 15","svd_oth 16","svd_oth 17","svd_oth 18","svd_oth 19","svd_oth 20","svd_oth 21","svd_oth 22","svd_oth 23","svd_oth 24","svd_oth 25","svd_oth 26","svd_oth 27","svd_oth 28","svd_oth 29","svd_oth 30","svd_oth 31","svd_oth 32","svd_oth 33","svd_oth 34","svd_oth 35","svd_oth 36","svd_oth 37","svd_oth 38","svd_oth 39","svd_oth 40","svd_oth 41","svd_oth 42","svd_oth 43","svd_oth 44","svd_oth 45","svd_oth 46","svd_oth 47","svd_oth 48","svd_oth 49","svd_oth 50"],axis=1)
#testSet = testSet.drop(["svd_tit.1","svd_tit.2","svd_tit.3","svd_tit.4","svd_tit.5","svd_tit.6","svd_tit.7","svd_tit.8","svd_tit.9","svd_tit.10","svd_tit.11","svd_tit.12","svd_tit.13","svd_tit.14","svd_tit.15","svd_tit.16","svd_tit.17","svd_tit.18","svd_tit.19","svd_tit.20","svd_tit.21","svd_tit.22","svd_tit.23","svd_tit.24","svd_tit.25","svd_tit.26","svd_tit.27","svd_tit.28","svd_tit.29","svd_tit.30","svd_tit.31","svd_tit.32","svd_tit.33","svd_tit.34","svd_tit.35","svd_tit.36","svd_tit.37","svd_tit.38","svd_tit.39","svd_tit.40","svd_tit.41","svd_tit.42","svd_tit.43","svd_tit.44","svd_tit.45","svd_tit.46","svd_tit.47","svd_tit.48","svd_tit.49","svd_tit.50","svd_dec.1","svd_dec.2","svd_dec.3","svd_dec.4","svd_dec.5","svd_dec.6","svd_dec.7","svd_dec.8","svd_dec.9","svd_dec.10","svd_dec.11","svd_dec.12","svd_dec.13","svd_dec.14","svd_dec.15","svd_dec.16","svd_dec.17","svd_dec.18","svd_dec.19","svd_dec.20","svd_dec.21","svd_dec.22","svd_dec.23","svd_dec.24","svd_dec.25","svd_dec.26","svd_dec.27","svd_dec.28","svd_dec.29","svd_dec.30","svd_dec.31","svd_dec.32","svd_dec.33","svd_dec.34","svd_dec.35","svd_dec.36","svd_dec.37","svd_dec.38","svd_dec.39","svd_dec.40","svd_dec.41","svd_dec.42","svd_dec.43","svd_dec.44","svd_dec.45","svd_dec.46","svd_dec.47","svd_dec.48","svd_dec.49","svd_dec.50","svd_bull.1","svd_bull.2","svd_bull.3","svd_bull.4","svd_bull.5","svd_bull.6","svd_bull.7","svd_bull.8","svd_bull.9","svd_bull.10","svd_bull.11","svd_bull.12","svd_bull.13","svd_bull.14","svd_bull.15","svd_bull.16","svd_bull.17","svd_bull.18","svd_bull.19","svd_bull.20","svd_bull.21","svd_bull.22","svd_bull.23","svd_bull.24","svd_bull.25","svd_bull.26","svd_bull.27","svd_bull.28","svd_bull.29","svd_bull.30","svd_bull.31","svd_bull.32","svd_bull.33","svd_bull.34","svd_bull.35","svd_bull.36","svd_bull.37","svd_bull.38","svd_bull.39","svd_bull.40","svd_bull.41","svd_bull.42","svd_bull.43","svd_bull.44","svd_bull.45","svd_bull.46","svd_bull.47","svd_bull.48","svd_bull.49","svd_bull.50","svd_bran.1","svd_bran.2","svd_bran.3","svd_bran.4","svd_bran.5","svd_bran.6","svd_bran.7","svd_bran.8","svd_bran.9","svd_bran.10","svd_bran.11","svd_bran.12","svd_bran.13","svd_bran.14","svd_bran.15","svd_bran.16","svd_bran.17","svd_bran.18","svd_bran.19","svd_bran.20","svd_oth 1","svd_oth 2","svd_oth 3","svd_oth 4","svd_oth 5","svd_oth 6","svd_oth 7","svd_oth 8","svd_oth 9","svd_oth 10","svd_oth 11","svd_oth 12","svd_oth 13","svd_oth 14","svd_oth 15","svd_oth 16","svd_oth 17","svd_oth 18","svd_oth 19","svd_oth 20","svd_oth 21","svd_oth 22","svd_oth 23","svd_oth 24","svd_oth 25","svd_oth 26","svd_oth 27","svd_oth 28","svd_oth 29","svd_oth 30","svd_oth 31","svd_oth 32","svd_oth 33","svd_oth 34","svd_oth 35","svd_oth 36","svd_oth 37","svd_oth 38","svd_oth 39","svd_oth 40","svd_oth 41","svd_oth 42","svd_oth 43","svd_oth 44","svd_oth 45","svd_oth 46","svd_oth 47","svd_oth 48","svd_oth 49","svd_oth 50"],axis=1)






#get  label and features
trainSetFeatures = trainSet.drop(['id', 'relevance'], axis=1).values  # id and relevance is not features to use
trainSetLabels = trainSet['relevance'].values

testSetFeatures = testSet.drop(['id', 'relevance'], axis=1).values
testSetLabels = testSet['relevance'].values


#k-best f-regression univariate feature selction
#RMSE :	0.507641492511
#trainSetFeatures = SelectKBest(f_regression, k=10).fit_transform(trainSetFeatures, trainSetLabels)
#testSetFeatures = SelectKBest(f_regression, k=10).fit_transform(testSetFeatures, testSetLabels)

#RMSE 0.505499650975
#trainSetFeatures = SelectKBest(f_regression, k=100).fit_transform(trainSetFeatures, trainSetLabels)
#testSetFeatures = SelectKBest(f_regression, k=100).fit_transform(testSetFeatures, testSetLabels)

#RMSE :	0.5289065508
#trainSetFeatures = SelectKBest(f_regression, k=150).fit_transform(trainSetFeatures, trainSetLabels)
#testSetFeatures = SelectKBest(f_regression, k=150).fit_transform(testSetFeatures, testSetLabels)

#RMSE : 0.508874063656
#trainSetFeatures = SelectKBest(f_regression, k=200).fit_transform(trainSetFeatures, trainSetLabels)
#testSetFeatures = SelectKBest(f_regression, k=200).fit_transform(testSetFeatures, testSetLabels)

#RMSE : RMSE :	0.508722146314
#trainSetFeatures = SelectKBest(f_regression, k=180).fit_transform(trainSetFeatures, trainSetLabels)
#testSetFeatures = SelectKBest(f_regression, k=180).fit_transform(testSetFeatures, testSetLabels)


print "\nBegin training..."
#train the model
random_forest_regressor = RandomForestRegressor(n_estimators=15, max_depth=100, random_state=0)
bagging_regressor = BaggingRegressor(random_forest_regressor, n_estimators=45, max_samples=0.1, random_state=25)
bagging_regressor.fit(trainSetFeatures, trainSetLabels)

print "\nBegin prediction..."
#make the prediction on the test set
predictedLabels = bagging_regressor.predict(testSetFeatures)

print "\nOutput the result..."
#output the prediction
testSetId = testSet['id']
pd.DataFrame({"id": testSetId, "relevance": predictedLabels}).to_csv('IOFolder/random_forest_results.csv', index=False)

print "RMSE :\t", utils.getRMSE(testSetLabels, predictedLabels)
print "MAE :\t", utils.getMAE(testSetLabels, predictedLabels)