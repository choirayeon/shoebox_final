import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from ast import literal_eval
from sklearn.decomposition import TruncatedSVD
from scipy.sparse.linalg import svds
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json

def data_loader(data):
    shoesData = pd.json_normalize(data)
    shoesData = shoesData.drop(['_id', 'userId', 'userName', 'age', 'gender', 'email', 'id', 'password'], axis=1)
    shoesData = shoesData.rename(columns={"shoesSizes.nike": "nike", "shoesSizes.adidas": "adidas", "shoesSizes.newBalance": "newBalance", "shoesSizes.vans": "vans", "shoesSizes.converse": "converse"})
    return shoesData

def roundTraditional(val, digits):
    return round(val+10**(-len(str(val))-1), digits)

def recommend_sizes(df_svd_preds, user_id, brands):
    sorted_user_predictions = roundTraditional(df_svd_preds.iloc[user_id-1][brands], -1)
    return sorted_user_predictions

def rs_system(data, user, brand):
    rs_data = data_loader(data)
    print(rs_data)
    
    m = rs_data.mean(axis=1)
    for i, col in enumerate(rs_data):
        rs_data.iloc[:, i] = rs_data.iloc[:, i].fillna(m)

    matrix = rs_data.to_numpy()
    sizes_mean = m.to_numpy()
    matrix_user_mean = matrix - sizes_mean.reshape(-1, 1)

    U, sigma, Vt = svds(matrix_user_mean, k = 4)
    sigma = np.diag(sigma)
    svd_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + sizes_mean.reshape(-1, 1)
    df_svd_preds = pd.DataFrame(svd_user_predicted_ratings, columns = rs_data.columns)

    predictions = recommend_sizes(df_svd_preds, user, brand)
    
    return predictions