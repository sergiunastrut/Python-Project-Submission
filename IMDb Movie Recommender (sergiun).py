# Importing Packages
import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
from tkinter import *
from tkinter import ttk

# Defining Headers
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
           "Accept-Encoding": "gzip, deflate",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1",
           "Connection": "close", "Upgrade-Insecure-Requests": "1"}

# Define List of Available Movie Genres
genres = [
    "Adventure",
    "Animation",
    "Biography",
    "Comedy",
    "Crime",
    "Drama",
    "Family",
    "Fantasy",
    "Film-Noir",
    "History",
    "Horror",
    "Music",
    "Musical",
    "Mystery",
    "Romance",
    "Sci-Fi",
    "Sport",
    "Thriller",
    "War",
    "Western"
]

# Scraping Top 25 Most Popular IMDb Movies in the Defined Genres
movie_list = []
unique_genre_list = []
url_dict = {}
file_name = "movielist.csv"
for genre in genres:
    url = "https://www.imdb.com/search/title/?genres={}&groups=top_1000"
    formatted_url = url.format(genre)
    url_dict[genre] = formatted_url


def get_movies(url, genre):
    resp = requests.get(url, headers=headers)
    content = BeautifulSoup(resp.content, 'lxml')

    for movie in content.select('.ipc-metadata-list-summary-item'):
        metascore = "0"
        if movie.findAll('span', 'sc-b0901df4-0 bcQdDJ metacritic-score-box'):
            metascore = movie.findAll('span', 'sc-b0901df4-0 bcQdDJ metacritic-score-box')[0].text.strip()
        try:
            movie_data = {
                "title": movie.select('.ipc-title__text')[0].get_text().strip(),
                "year": movie.findAll('span', 'sc-b189961a-8 kLaxqf dli-title-metadata-item')[0].text.strip(),
                "certification": movie.findAll('span', 'sc-b189961a-8 kLaxqf dli-title-metadata-item')[2].text.strip(),
                "runtime": movie.findAll('span', 'sc-b189961a-8 kLaxqf dli-title-metadata-item')[1].text.strip(),
                "genre": genre,
                "imdb_rating": movie.findAll('span',
                                        'ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating')[
                    0].text.strip(),
                "metascore": metascore,
                "plot": movie.select('.ipc-html-content-inner-div')[0].get_text().strip(),
                "number_of_votes": movie.findAll('span', 'ipc-rating-star--voteCount')[0].text.strip()
            }
        except IndexError:
            continue
        movie_list.append(movie_data)


# Pushing Scraped Data to CSV
for genre, url in url_dict.items():
    get_movies(url, genre)
    movie_dataframe = pd.DataFrame(movie_list)
    movie_dataframe.to_csv(file_name)
    print("Scraped & Appended Top 25 Most Popular", genre, "Movies")

# Processing CSV Data for App Usage
class data_processing:
    def __init__(self):
        self.movie_df = pd.read_csv('movielist.csv', sep=',')

        # Generate an unique genre list for users to input
        self.unique_genre_list = []
        for genre in self.movie_df['genre']:
            for gen in genre.split(', '):
                self.unique_genre_list.append(gen)
        self.unique_genre_list = list(set(self.unique_genre_list))

    def recommend_a_movie(self, selected_genre):
        # Filter the DataFrame to get the movies that contain our selected genre
        genre_df = self.movie_df[self.movie_df['genre'].str.contains(selected_genre)]
        genre_df.reset_index(drop=True, inplace=True)

        # Selected a random index of DataFrame to get a movie
        random_index = random.randint(0, genre_df.shape[0]-1)
        selected_df = genre_df.loc[random_index]

        # Return selected movie information as a dictionary
        movie_dict = {
            'title': selected_df['title'],
            'year': selected_df['year'],
            'certification': selected_df['certification'],
            'runtime': selected_df['runtime'],
            'genre': selected_df['genre'],
            'imdb_rating': selected_df['imdb_rating'],
            'metascore': selected_df['metascore'],
            'number_of_votes': selected_df['number_of_votes'],
            'plot': selected_df['plot']
        }
        return movie_dict


if __name__ == '__main__':
    DP = data_processing()

    unique_genre_list = DP.unique_genre_list
    print(f'The available list of movie genres is:', unique_genre_list)


# Initiating our data processing function
DP = data_processing()
unique_genre_list = DP.unique_genre_list

# Building the Tkinter App
root = Tk()
root.title('Movie Recommender Based on Genre & Popularity')
root.geometry(f'1200x700')
root.config(background="#1DEBF8")


def tk_row(row, key, value):
    # Defining a function to display the movie info on the app
    Label(text=key, height='2', width="20", font=("Arial", 14, 'bold'), bg='#1DEBF8', anchor="w").grid(row=row, column=0)
    Label(text=value, height='3', width="100", font=("Arial", 12), bg='#1DEBF8', anchor="w", wraplength=800, justify='left').grid(row=row, column=1)


def recommend():
    # Getting the selected genre
    global selected_genre
    selected_genre = var.get()
    if selected_genre == '':
        return None

    # Invoking our data processing function to recommend a movie and display it on the app
    movie_info = DP.recommend_a_movie(selected_genre)
    tk_row(30, '', '')
    tk_row(31, 'Movie name', movie_info['title'])
    tk_row(32, 'Year', movie_info['year'])
    tk_row(33, 'Certification', movie_info['certification'])
    tk_row(34, 'Runtime', movie_info['runtime'])
    tk_row(35, 'IMDb Rating', movie_info['imdb_rating'])
    tk_row(36, 'Metascore', movie_info['metascore'])
    tk_row(37, 'Number of Votes', movie_info['number_of_votes'])
    tk_row(38, 'Plot', movie_info['plot'])


# Constructing the banner and user selection area
banner = Label(text=f'Select a genre you are interested in.\nWe will recommend a popular movie based on that for you.', font=("Arial", 16, 'bold'), width=100, height=2, bg='#283442', fg='white',)
banner.grid(row=0, column=0, columnspan=2)
var = StringVar()
Label(text="Select a genre:", height="2", width="20", font=("Arial", 14, 'bold'), bg='#1DEBF8', anchor="w").grid(row=5, column=0)
ttk.Combobox(textvariable=var, values=unique_genre_list, height=10, width=40, state='readonly').grid(row=5, column=1)
button = Button(text="Suggest Movie", bg="#D3D3D3", font="Arial", width="12", height="1", command=recommend)
button.grid(row=7, column=1)

# Starting the movie recommender app
root.mainloop()