import streamlit as st
from content_based_filtering import content_recommendation
from scipy.sparse import load_npz
import pandas as pd 
from collaborative_filtering import collaborative_recommendation
from numpy import load
from hybrid_recommendation import HybridRecommenderSystem

# load the data
cleaned_data_path = "data/cleaned_data.csv"
st.session_state.songs_data = pd.read_csv(cleaned_data_path)

#load the transformed data
transformed_data_path = "data/transformed_data.npz"
st.session_state.transformed_data = load_npz(transformed_data_path)

# load the track ids
track_ids_path = "data/track_ids.npy"
st.session_state.track_ids = load(track_ids_path,allow_pickle=True)

# load the filtered songs data
filtered_data_path = "data/collab_filtered_data.csv"
st.session_state.filtered_data = pd.read_csv(filtered_data_path)

# load the interaction matrix
interaction_matrix_path = "data/interaction_matrix.npz"
st.session_state.interaction_matrix = load_npz(interaction_matrix_path)

# load the transformed hybrid data
transformed_hybrid_data_path = "data/transformed_hybrid_data.npz"
st.session_state.transformed_hybrid_data = load_npz(transformed_hybrid_data_path)

##APP header
st.markdown(
    """
    <style>
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .animated-title {
        font-size: 46px;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(
            270deg,
            #1DB954,
            #1ed760,
            #00ffaa
        );
        background-size: 600% 600%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient 6s ease infinite;
    }
    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #b3b3b3;
        margin-top: 6px;
    }
    </style>

    <div class="animated-title">🎵 Spotify Song Recommender</div>
    <div class="subtitle">
        Discover personalized and diverse music recommendations
    </div>
    <hr>
    """,
    unsafe_allow_html=True
)
####LAYOYT END###

## slider
st.markdown("### 🔍 Song Details")

col1, col2 = st.columns(2)

with col1:
    song_name = st.text_input(
        "🎶 Song Name",
        placeholder="e.g. Beat it",
        help="Type the exact song name as it appears on Spotify"
    )

with col2:
    artist_name = st.text_input(
        "🎤 Artist Name",
        placeholder="e.g. Michael Jackson",
        help="Enter the primary artist name"
    )

st.markdown("### 🎯 Recommendation Count")

k = st.select_slider(
    "Number of songs to recommend",
    options=[5, 10, 15, 20],
    value=10
)

# Normalize input
song_name = song_name.strip().lower()
artist_name = artist_name.strip().lower()

###slider

if ((st.session_state.filtered_data["name"] == song_name) & (st.session_state.filtered_data["artist"] == artist_name)).any():
    st.markdown("### ⚙️ Recommendation Settings")

    filtering_type = st.selectbox(
        label='Select recommendation method',
        options=[
            'Content-Based Filtering',
            'Collaborative Filtering',
            'Hybrid Recommender System'
        ],
        index=2
    )

    # Diversity slider
    st.markdown("#### 🎚️ Recommendation Style")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("⬅️ **Personalized**")
    with col2:
        st.markdown(
            "<div style='text-align: right'>Diverse ➡️</div>",
            unsafe_allow_html=True
        )

    diversity = st.slider(
        label="",
        min_value=1,
        max_value=10,
        value=5,
        step=1
    )

    content_based_weight = 1 - (diversity / 10)


else:
    #type of filtering 
    filtering_type = st.selectbox(label= 'Select the type of filtering:', 
                                options= ['Content-Based Filtering'])
    

# ✅ BUTTON GOES HERE
st.markdown("<br>", unsafe_allow_html=True)
get_rec = st.button(
    "🎧 Get Recommendations",
    use_container_width=True,
    disabled=not (song_name and artist_name)
)

#button
if filtering_type == 'Content-Based Filtering':
    if get_rec:
        if ((st.session_state.songs_data["name"] == song_name) & (st.session_state.songs_data['artist'] == artist_name)).any():
            st.write('Recommendations for', f"**{song_name}** by **{artist_name}**")
            with st.spinner("Finding the perfect tracks for you 🎶"):
                recommendations =content_recommendation(song_name=song_name,
                                                    artist_name=artist_name,
                                                    songs_data=st.session_state.songs_data,
                                                    transformed_data=st.session_state.transformed_data,
                                                    k=k
                )

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


elif filtering_type == 'Collaborative Filtering':
    if get_rec:
        if ((st.session_state.filtered_data["name"] == song_name) & (st.session_state.filtered_data["artist"] == artist_name)).any():
            st.write('Recommendations for', f"**{song_name}** by **{artist_name}**")
            with st.spinner("Finding the perfect tracks for you 🎶"):
                recommendations = collaborative_recommendation(song_name=song_name,
                                                            artist_name=artist_name,
                                                            track_ids=st.session_state.track_ids,
                                                            songs_data=st.session_state.filtered_data,
                                                            interaction_matrix=st.session_state.interaction_matrix,
                                                            k=k)
            

            # Display Recommendations
            for ind , recommendation in recommendations.iterrows():
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

elif filtering_type == "Hybrid Recommender System":
    if get_rec:
        if ((st.session_state.filtered_data["name"] == song_name) & (st.session_state.filtered_data["artist"] == artist_name)).any():
            st.write('Recommendations for', f"**{song_name}** by **{artist_name}**")
            recommender = HybridRecommenderSystem(
                              number_of_recommendations= k,
                              weight_content_based = content_based_weight)
            
            # get the recommendations
            with st.spinner("Finding the perfect tracks for you 🎶"):
                recommendations = recommender.give_recommendations(song_name=song_name,
                                                                artist_name=artist_name,
                                                                songs_data=st.session_state.filtered_data,
                                                                transformed_matrix=st.session_state.transformed_hybrid_data,
                                                                track_ids= st.session_state.track_ids,
                                                                interaction_matrix= st.session_state.interaction_matrix)
                
            # Display Recommendations
            for ind , recommendation in recommendations.iterrows():
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
        






