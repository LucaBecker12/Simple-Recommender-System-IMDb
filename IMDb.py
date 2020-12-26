import requests
import os
from bs4 import BeautifulSoup

# URLS for Amazon Prime and Netflix recommondations by IMDb
PRIME_URL = 'https://www.imdb.com/imdbpicks/new-on-prime-video-streaming/ls083285204/?ref_=watch_wchgd_1_2_m_wtw_prime&sort=moviemeter,asc&st_dt=&mode=detail&page=1'
NETFLIX_URL = 'https://www.imdb.com/whats-on-tv/new-on-netflix-streaming/ls083287995/?ref_=watch_wchgd_1_5_m_wtw_netflix&sort=moviemeter,asc&st_dt=&mode=detail&page=1'

start_prompt = '''
Hello welcome to the IMDb Movie recommender 
Do you wish to find movies on Prime or Netflix?
p - Prime
n - Netflix
q - Quit
Enter your option: '''

prompt = '''
.............................
    Enter key to continue
.............................
'''

movie_number_prompt = '''
How many suggestions would you like to see?
Between 1 and {}
What is your number?
'''

def get_movies(URL):
    # Load page via requests nodule
    page = requests.get(URL)

    # Parser Html per lxml parser into BeautifulSoup object and select all movies
    soup = BeautifulSoup(page.content, features="lxml")
    raw_data = soup.find_all('div', attrs={"class": "lister-item mode-detail"})

    # Filter important data from movies (title, description, rating)
    # Save them in accessible format
    movies = []
    for item in raw_data:
        movie = dict()
        movie["title"] = item.find('h3', attrs={"class": "lister-item-header"}).find('a').text.strip()
        movie["description"] = item.find_all("p")[1].text.strip()
        rating = item.find('div', attrs={"class": "lister-item-content"}).find('div', attrs={"class": "inline-block ratings-imdb-rating"})
        
        # Check if rating is existent
        if rating != None:
            movie["rating"] = rating.text.strip()
        else:
            movie["rating"] = "-1"

        movies.append(movie)
    return movies

def main():
    # Ask User which movie provider he/ she wants to check
    selected = input(start_prompt).lower()
    while selected != 'q':
        if selected == 'p':
            movies = get_movies(PRIME_URL)
        elif selected == 'n':
            movies = get_movies(NETFLIX_URL)
        else:
            print('Command not found.')
            selected = 'q'
            continue

        printMovies(movies)
        selected = input(prompt).lower()

def printMovies(movies):
    # Ask user how many movies he/ she wants to see
    num_movies = int(input(movie_number_prompt.format((len(movies)))))
    if num_movies > len(movies): num_movies = len(movies)
    os.system('cls')

    # Print movies in wanted range
    for i in range(num_movies):
        keys = movies[i].keys()
        vals = movies[i].values()
        print(f'{i+1}.')
        for key, val in zip(keys, vals):
            # Replace negative ratings with "Not found"
            if key == "rating" and val == "-1":
                val = "Not found"
            print(f' {key.capitalize()}: {val}')
        print()

if __name__ == "__main__":
    main()