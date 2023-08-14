import os
from dotenv import load_dotenv
import requests
from typing import Optional, List, Tuple


class OMDBApi:

    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("API_KEY")
        self.url = "https://www.omdbapi.com"

    def _images_path(self, title: str) -> Optional[Tuple[str, str, str, str]]:
        """
        Helper function to fetch data about an image and movie from the OMDB API.

        Parameters:
            title (str): The movie title.

        Returns:
            Optional[Tuple[str, str, str, str]]: A tuple containing the image URL (poster),
                                                 release date, runtime, and plot description.
        """
        params = {
            "apikey": self.api_key,
            "t": title
        }

        response = requests.get(self.url, params=params)
        data = response.json()

        if response.status_code == 200 and data.get("Poster"):
            # Extract release date, runtime, and plot from API data
            released = data.get("Released", "")
            runtime = data.get("Runtime", "")
            plot = data.get("Plot", "")
            # Return the poster URL, release date, runtime, and plot description
            return data["Poster"], released, runtime, plot
        else:
            return None, "", "", ""

    def get_movie_info(self, titles: List[str]) -> List[dict]:
        """
        Get information about a movie from the OMDB API.

        Parameters:
            titles (List[str]): A list of movie titles.

        Returns:
            List[dict]: A list of dictionaries containing information about the movies,
                        including title, poster, release date, runtime, and plot description.
        """
        movie_info_list = []
        for title in titles:
            path, released, runtime, plot = self._images_path(title)  # Extract plot from the _images_path function
            movie_info_list.append({
                "title": title,
                "poster": path,
                "released": released,
                "runtime": runtime,
                "plot": plot
            })
        return movie_info_list

    def get_posters(self, titles: List[str]) -> List[str]:
        """
        Get image URLs (posters) for a list of movies.

        Parameters:
            titles (List[str]): A list of movie titles.

        Returns:
            List[str]: A list of image URLs (posters).
        """
        posters = []
        released_list = []  # Create a list to store movie release years
        runtime_list = []  # Create a list to store movie runtimes
        plot_list = []  # Create a list to store movie plot descriptions

        for title in titles:
            path, released, runtime, plot = self._images_path(title)
            if path:  # If the image doesn't exist
                posters.append(path)
            else:
                posters.append('assets//none.jpeg')  # Add a placeholder image
            released_list.append(released)  # Add the movie release year to the list
            runtime_list.append(runtime)  # Add the movie runtime to the list
            plot_list.append(plot)  # Add the movie plot description to the list
        return posters, released_list, runtime_list

