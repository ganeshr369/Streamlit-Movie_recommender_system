import streamlit as st
import pandas as pd
import joblib

movies = joblib.load("movies_filtered.pkl")

all_genres = sorted(set(genre for sublist in movies["genres"].str.split('|') for genre in sublist))

st.set_page_config(
    page_icon="🎬",
    page_title="Movie Recommender System | Ganesh Rawat"
)

st.markdown("<h1 style='text-align: center; color: #f63366;'>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)
st.write("Get Amazing movie Suggestion based on genres and high ratings")

movie_list = movies["title"].values
selected_genres = st.multiselect("Choose a movie you would like", all_genres)

def recommend(selected_genres, top_n=10):
    if not selected_genres:
        return []
    mask = movies["genres"].apply(lambda x: any(genre in x.split('|') for genre in selected_genres))
    filtered_movies = movies[mask]
    top_movies = filtered_movies.sort_values(by="avg_rating", ascending=False).head(top_n)
    return top_movies[['title', 'genres', 'avg_rating']]
   
if st.button("Get Recommendations"):
    results = recommend(selected_genres)
    if not results.empty:
        st.subheader("💫 Recommended Movies:")
        for i, row in results.iterrows():
            st.markdown(f"**{row['title']}** Genres: {row['genres']}, Avg Rating {row['avg_rating']:.2f}")
    else:
        st.warning("No Movies Found for this Selected Genres!")