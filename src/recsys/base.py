from typing import List, Set, Optional
import pandas as pd
import numpy as np
import streamlit as st
from .utils import parse

@st.cache_data
def load_base(path: str, index_col: str = 'movie_id') -> pd.DataFrame:
    """
    Loads the base data from a CSV file into a DataFrame.

    Parameters:
        path (str): The file path of the CSV.
        index_col (str): The name of the column to be used as the index in the DataFrame.

    Returns:
        pd.DataFrame: The loaded DataFrame.
    """
    data_base = pd.read_csv(path, index_col=index_col)
    data_base.index = data_base.index.astype(int)
    return data_base


class ContentBaseRecSys:

    def __init__(self, movies_dataset_filepath: str, distance_filepath: str):
        """
        Initializes the ContentBaseRecSys class.

        Parameters:
            movies_dataset_filepath (str): The file path of the movies dataset CSV file.
            distance_filepath (str): The file path of the distance CSV file.
        """
        self.distance_total = load_base(distance_filepath, index_col='movie_id')
        self.distance_total.columns = self.distance_total.columns.astype(int)
        self.distance = self.distance_total
        self._init_movies(movies_dataset_filepath)

    def _init_movies(self, movies_dataset_filepath: str) -> None:
        """
        Initializes the movies dataset.

        Parameters:
            movies_dataset_filepath (str): The file path of the movies dataset CSV file.
        """
        self.movies_total = load_base(movies_dataset_filepath, index_col='movie_id')
        self.movies_total.index = self.movies_total.index.astype(int)
        self.movies_total['genres'] = self.movies_total['genres'].apply(parse)
        self.movies = self.movies_total

    def get_title(self) -> List[str]:
        """
        Returns a list of movie titles.

        Returns:
            List[str]: The list of movie titles.
        """
        return self.movies_total['title'].values

    def get_genres(self) -> Set[str]:
        """
        Returns a set of movie genres.

        Returns:
            Set[str]: The set of movie genres.
        """
        genres = [item for sublist in self.movies_total['genres'].values.tolist() for item in sublist]
        return set(genres)

    def get_vote_average(self) -> List[float]:
        """
        Returns a list of movie vote averages.

        Returns:
            List[float]: The list of movie vote averages.
        """
        return self.movies_total['vote_average'].values

    def filters(self, genre: str, vot_ave: Optional[float]) -> None:
        """
        Applies filters to the movies DataFrame.

        Parameters:
            genre (str): The selected genre to filter the movies.
            vot_ave (Optional[float]): The selected vote average to filter the movies (None if not selected).
        """
        self.movies = self.movies_total
        if vot_ave is not None:
            self.movies = self.movies.loc[self.movies['vote_average'] >= vot_ave]
        if genre:
            self.movies = self.movies.loc[self.movies.genres.apply(
                lambda x: genre in x)]
        self.distance = self.distance.loc[self.movies.index]

    def remove_filters(self) -> None:
        """
        Removes all filters applied to the movies DataFrame.
        """
        self.movies = self.movies_total
        self.distance = self.distance_total

    def recommendation(self, title: str, top_k: int = 5) -> List[str]:
        """
        Returns the names of the top_k most similar movies with the movie "title".

        Parameters:
            title (str): The title of the movie to get recommendations for.
            top_k (int): The number of top similar movies to retrieve (default is 5).

        Returns:
            List[str]: The list of recommended movie titles.
        """
        ind = pd.Series(self.movies_total.index, index=self.movies_total['title']).drop_duplicates()
        idx = ind[title]
        sim_scores = list(enumerate(self.distance[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:top_k+1]
        movie_indices = [i[0] for i in sim_scores]
        return list(self.movies['title'].iloc[movie_indices])