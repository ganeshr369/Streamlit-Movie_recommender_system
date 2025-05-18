import streamlit as st
import pandas as pd
import joblib
from fuzzywuzzy import process
import random

movies = joblib.load("movies_filtered.pkl")
all_genres = sorted(set(genre for sublist in movies["genres"].str.split('|') for genre in sublist))

st.set_page_config(
    page_icon="🎬",
    page_title="Movie Recommender System | Ganesh Rawat"
)

st.markdown("<h1 style='text-align: center; color: #f63366;'>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)
st.write("This is designed to suggest movies to users based on your input (movie genres).🎬 Explore a variety of movie recommendations from action-packed adventures to heartwarming romances. Choose your favorite genres, hit the **Get Recommendations** button, and let me show you the magic! 💥 I hope you enjoy your movie journey.\n Don't forget to share your recommendations with friends!")
st.markdown("<p style='color: #1e81b0;'> Get Amazing movie Suggestion based on genres and high ratings </p>", unsafe_allow_html=True)

movie_list = movies["title"].values
acol1, acol2 = st.columns([2,2])
with acol1:
    st.image("https://img.freepik.com/free-photo/people-cinema-watching-movie_23-2151005484.jpg")
with acol2:
    user_input = st.text_input(" Search for a movie 🔍")
    if user_input:
        suggestions = process.extract(user_input, movie_list, limit=5)
        selected_movie = st.selectbox("Did you mean:", [s[0] for s in suggestions])
selected_genres = st.multiselect("Choose a movie genres you would like", all_genres)

def recommend(selected_genres, top_n=10):
    if not selected_genres:
        return []
    mask = movies["genres"].apply(lambda x: any(genre in x.split('|') for genre in selected_genres))
    filtered_movies = movies[mask]
    top_movies = filtered_movies.sort_values(by="avg_rating", ascending=False).head(top_n)
    return top_movies[['title', 'genres', 'avg_rating']]
   
if st.button("Get Recommendations"):
    results = recommend(selected_genres)
    if isinstance(results, pd.DataFrame) and not results.empty:
        st.subheader("💫 Recommended Movies:")
        for i, row in results.iterrows():
            st.markdown(f"**{row['title']}** Genres: {row['genres']}, Avg Rating {row['avg_rating']:.2f}")
    elif isinstance(results, list) not in results:
        st.warning("Invalid Input! or No Movies Found for this Selected Genres!")

st.markdown("---")
bcol1, bcol2 = st.columns([2,2])
with bcol1:
    st.write("Pick a Random High Rated Movie here 👉")
with bcol2:
    if st.button("🎲 Surprize Me"):
        top_movies = movies[movies['avg_rating']>=4.5]
        random_movies = random.choice(top_movies['title'].tolist())
        st.success(f"How about 👉 **{random_movies}**")
        
st.markdown("---")
st.markdown("""Made with ❤️ Ganesh Rawat <a href="https://www.ganeshrawat.com.np">🌐</a> """,unsafe_allow_html=True)