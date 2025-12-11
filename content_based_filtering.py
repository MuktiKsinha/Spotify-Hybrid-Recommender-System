import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import MinMaxScaler,OneHotEncoder,StandardScaler
from category_encoders import CountEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer
from sklearn.metrics.pairwise import cosine_similarity
from data_cleaning import data_for_content_filtering
from scipy.sparse import save_npz

# Cleaned Data Path
CLEANED_DATA_PATH = "data/cleaned_data.csv"

#columns to transform
frequency_encode_cols  = ['year']
ohe_cols = ['artist','time_signature',"key"]
tfidf_col = 'tags'
standard_scale_cols = ["duration_ms","loudness","tempo"]
min_max_scale_cols = ["danceability","energy","speechiness","acousticness","instrumentalness","liveness","valence"]

def train_transformer(data):
    # transform the data
    transformer = ColumnTransformer(
        transformers=[
            ("frequency_encode_cols",CountEncoder(normalize=True, return_df=True),frequency_encode_cols),
            ("ohe",OneHotEncoder(handle_unknown="ignore"),ohe_cols),
            ("tfidf",TfidfVectorizer(max_features=85),tfidf_col),    #refer # unique tags in the data more tha 1000 its has 85
            ("standard_scale",StandardScaler(),standard_scale_cols),
            ("min_max_scale",MinMaxScaler(),min_max_scale_cols)
        ],remainder = 'passthrough',n_jobs =-1,force_int_remainder_cols =False
)

    # fit the data
    transformer.fit(data)
    # save the transformer
    joblib.dump(transformer,"transformer.joblib")


def transform_data(data):
    # load the transformer 
    transformer = joblib.load("transformer.joblib")

    #transform the data
    transformed_data = transformer.transform(data)

    return transformed_data

def save_transformed_data(transformed_data,save_path):
    #save the transformed data
    save_npz(save_path,transformed_data)

def calculate_cosine_similarity(input_vector,data):
    # calculate similarity score 
    similarity_score  = cosine_similarity(input_vector,data)
    return similarity_score

def content_recommendation(song_name,artist_name,songs_data,transformed_data,k=10):
    #convert song name to lower case 
    song_name = song_name.lower()
     # convert the artist name to lowercase
    artist_name = artist_name.lower()
    
    #filter out the song from data
    song_row = songs_data.loc[(songs_data["name"] == song_name) & (songs_data["artist"] == artist_name)]

    #get the index of the song
    song_index = song_row.index[0]
    #genrate the input vector
    input_vector = transformed_data[song_index].reshape(1,-1)
    #calculate the similarity score
    similarity_scores = cosine_similarity(input_vector,transformed_data)
    # get top k songs
    top_k_songs_indexes=np.argsort(similarity_scores.ravel())[-11:][::-1]
    #get the top k songs name
    top_k_songs_names = songs_data.iloc[top_k_songs_indexes]
    #print the top k songs
    top_k_list = top_k_songs_names[['name','artist','spotify_preview_url']].reset_index(drop=True)
    return top_k_list


def main(data_path):

    # load the data
    data = pd.read_csv(data_path)
   
    # clean the data
    data_content_filtering = data_for_content_filtering(data)
    
    #transform the data
    train_transformer(data_content_filtering)
    
    #transform the data
    transformed_data = transform_data(data_content_filtering)
    
    #save the data
    save_transformed_data(transformed_data,"data/transformed_data.npz")
   
    
if __name__ == "__main__":
    main(CLEANED_DATA_PATH)
