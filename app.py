import streamlit as st
from content_based_filtering import recommend
from scipy.sparse import load_npz
import pandas as pd 

#rransform the data
transformed_data_path = "data/transformed_data.npz"

# cleaned data path
cleaned_data_path = "data/cleaned_data.csv"

# load the data
data = pd.read_csv(cleaned_data_path)

#load the transformed data
transformed_data = load_npz(transformed_data_path)

#title
st.title('Welcome to the Spotify Song Recommender!')

# subheader
st.subheader('### Enter the name of a song and the recommender will suggest similar songs 🎵🎧')

#text input
song_name = st.text_input('Enter a song name')
st.write('You entered:',song_name)


# k reccomendations
k = st.selectbox('How many recommendations do you want?', [5,10,15,20], index=1)

#button
if st.button('Get Recommendations'):
    if (data['name']== song_name).any():
        st.write("Recommendation for",f"***{song_name}***")
        recommendations =recommend(song_name,data,transformed_data,k)

        #display recommmendation
        for ind,recommendation in recommendations.iterrows():
            song_name = recommendation['name'].title()
            artist_name = recommendation['artist'].title()

            if ind == 0:
                st.markdown("## Currently Playing")
                st.markdown(f"#### **{song_name}** by **{artist_name}**")
                st.audio(recommendation['spotify_preview_url'])
                st.write('---')
            elif ind == 1:   
                st.markdown("### Next Up 🎵")
                st.markdown(f"#### {ind}. **{song_name}** by **{artist_name}**")
                st.audio(recommendation['spotify_preview_url'])
                st.write('---')
            else:
                st.markdown(f"#### {ind}. **{song_name}** by **{artist_name}**")
                st.audio(recommendation['spotify_preview_url'])
                st.write('---')
        
    else:
        st.write(f"Sorry, we couldn't find {song_name} in our database. Please try another song.")






