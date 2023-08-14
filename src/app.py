import os
from dotenv import load_dotenv
import streamlit as st
import base64
from streamlit_extras.no_default_selectbox import selectbox
from api.omdb import OMDBApi
from recsys import ContentBaseRecSys

TOP_K = 5
load_dotenv()

# Load environment variables
MOVIES = os.getenv("MOVIES")
DISTANCE = os.getenv("DISTANCE")
API_KEY = os.getenv("API_KEY")

# Initialize OMDBApi and ContentBaseRecSys instances
omdbapi = OMDBApi()
recsys = ContentBaseRecSys(
    movies_dataset_filepath=MOVIES,
    distance_filepath=DISTANCE,
)

# Title and introductory GIF
st.markdown(
    "<h1 style='text-align: center; color: white; font-size: 35px; transform: scale(2, 1.5);'>Welcome to the best recommendation service!</h1>",
    unsafe_allow_html=True
)

file = open("..\\misc\\images\\cinema.gif", "rb")
contents = file.read()
data_url = base64.b64encode(contents).decode("utf-8")
file.close()

st.image(f'data:image/gif;base64,{data_url}', use_column_width=True)

# Title for movie recommender service
st.markdown(
    "<h1 style='text-align: center; color:white;'>Movie Recommender Service</h1>",
    unsafe_allow_html=True
)

# Select or type a movie and display movie info
selected_movie = selectbox(
    "Type or select a movie you like:",
    recsys.get_title()
)

if selected_movie:
    movie_info_list = omdbapi.get_movie_info([selected_movie])
    movie_info = movie_info_list[0]
    # Display the movie poster and information in columns
    col_poster, col_info = st.columns([1, 3])
    with col_poster:
        st.image(movie_info['poster'], use_column_width=True)
    with col_info:
        st.write("Title:", movie_info['title'])
        st.write("Released:", movie_info['released'])
        st.write("Runtime:", movie_info['runtime'])
        st.write("Plot:", movie_info['plot'])

# Genre and vote average filters
filt_col = st.columns([3, 3])
with filt_col[0]:
    selected_genre = selectbox(
        "Type or select a genre you like:",
        recsys.get_genres()
    )
with filt_col[1]:
    vote_average_range = st.slider(
        "Select vote average:",
        min_value=0.0,
        max_value=10.0,
        step=0.1,
    )

# Apply filters based on selected_genre and vote_average_range
if selected_genre or vote_average_range:
    recsys.filters(selected_genre, vote_average_range)
else:
    recsys.remove_filters()

# Show recommendation button
start = st.button('Show Recommendation')

if start:
    if selected_movie:
        recommended_movie_names = recsys.recommendation(
            selected_movie, top_k=TOP_K)
        if len(recommended_movie_names) == 0:
            st.write('Sorry, no recommendations.')
        else:
            st.write("Recommended Movies:")
            recommended_movie_info = omdbapi.get_movie_info(recommended_movie_names)
            movies_col = st.columns(len(recommended_movie_names))
            for index, col in enumerate(movies_col):
                with col:
                    st.image(recommended_movie_info[index]['poster'])
                    st.markdown(f"<h3 style='color:white; font-size: 20px;'>\
                        {recommended_movie_info[index]['title']}</h3>", unsafe_allow_html=True)
                    st.write("Released:", recommended_movie_info[index]['released'])
                    st.write("Runtime:", recommended_movie_info[index]['runtime'])

# Final GIF and message
file_2 = open("..\\misc\\images\\prog.gif", "rb")
contents_2 = file_2.read()
data_url_2 = base64.b64encode(contents_2).decode("utf-8")
file_2.close()

st.image(f'data:image/gif;base64,{data_url_2}', use_column_width=True)

st.markdown(
    "<h2 style='text-align: center; color: red; font-size: 40px'>A good choice! Enjoy watching!</h2>",
    unsafe_allow_html=True
)
