"""
CMPUT 174 Lab 9 'Shows4' Program
Uses an API to Let User Search For TV Shows, Then Lets User Pick a Show and Specific Season With Episode Titles and Ratings
Author: Abdullah Faisal
When: November 23, 2022
"""

# import statements
import requests
import pprint
import json
# Uncomment two lines below if you get status code 429 (rate limit exceeded)
# import requests_cache
# requests_cache.install_cache('cmput174_cache')

# global variable
BASE_URL = "https://api.tvmaze.com/"


# searches for TV shows using the TV Maze API, returns list of dict. If show not found, returns None
def get_shows(query: str) -> list[dict]:
    endpoint_url = f"{BASE_URL}/search/shows?q={query}"
    response = requests.get(endpoint_url)  # sends request to url
    info = response.json()  # reads response and stores data in info
    if info == []:
        return None
    return info


# formats the show names
def format_show_name(show: dict) -> str:
    nested_dict = show["show"]
    if nested_dict['premiered'] == None:
        premiered = '?'
    else: premiered = nested_dict['premiered'][0:4]
    if nested_dict['ended'] == None:
        ended = '?'
    else: ended = nested_dict['ended'][0:4]
    genres = nested_dict['genres']
    if genres == []:
        genres = ['?']
    return(f"({premiered} - {ended}, {', '.join(genres)})")


# gets and returns seasons info in list of dict. If seasons not found, returns None
def get_seasons(show_id: int) -> list[dict]:
    endpoint_url = f"{BASE_URL}shows/{show_id}/seasons"
    response = requests.get(endpoint_url)  # sends request to url
    info = response.json()  # reads response and stores data in info
    if info == []:
        return None
    return info  


# formats the season names
def format_season_name(season: dict) -> str:
    number = season['number']
    if season['premiereDate'] == None:
        premiereDate = '?'
    else: premiereDate = season['premiereDate'][0:4]
    if season['endDate'] == None:
        endDate = '?'
    else: endDate = season['endDate'][0:4]
    if season['episodeOrder'] == None:
        episodeOrder = '?'
    else: episodeOrder = season['episodeOrder']     
    return(f"Season {number} ({premiereDate} - {endDate}), {episodeOrder} episodes")


# calls get_seasons and format_season_name functions to display the seasons of a show
def display_seasons(results: list[dict], user_input: int) -> list[dict]:
    find_show = results[user_input - 1]["show"]
    show_id = find_show['id']
    print(f"Seasons of {find_show['name']}:")
    seasons = get_seasons(show_id)
    n = 1
    for season in seasons:
        print(f"{n}. {format_season_name(seasons[n-1])}")  # prints all seasons in a show with relevant info
        n += 1
    return seasons


# gets and returns episodes info in list of dict. If episodes not found, returns None
def get_episodes_of_season(season_id: int) -> list[dict]:
    endpoint_url = f"{BASE_URL}seasons/{season_id}/episodes"
    response = requests.get(endpoint_url)  # sends request to url
    info = response.json()  # reads response and stores data in info
    if info == []:
        return None
    return info      


# formats the episode names
def format_episode_name(episode: dict) -> str:
    number = episode['number']
    if episode['name'] == None:
        name = '?'
    else: name = episode['name']
    if episode['rating'] == None:
        rating = '?'
    else: 
        rating = episode['rating']
        rating = rating['average']
    return (f"E{number} {name} (rating: {rating})")    


# calls get_episodes_of_season function to help display the episodes of a season
def display_episodes(seasons: list[dict], user_input: int, user_show_input: int, results: list[dict]) -> list[dict]:
    find_show = results[user_show_input - 1]["show"]
    find_season = seasons[user_input - 1]
    season_id = find_season['id']
    print(f"Episodes of {find_show['name']} S{find_season['number']}:")
    episodes = get_episodes_of_season(season_id)
    return episodes


# calls all functions to run program
def main():
    query = input("Search for a show: ")
    results = get_shows(query)
    if not results:
        print("No results found")
    else:
        n = 1
        print("Here are the results:")
        for result in results:
            show = result["show"]
            print(f"{n}. {show['name']}", format_show_name(results[n-1]))  # prints show results from user search
            n += 1
        user_show_input = int(input('Select a show: '))
        seasons = display_seasons(results, user_show_input)
        user_season_input = int(input('Select a season: '))        
        episodes = display_episodes(seasons, user_season_input, user_show_input, results)
        n = 1
        for episode in episodes:
            print (f"{n}. S{user_season_input}" + format_episode_name(episodes[n-1]))  # prints all episodes in a season with relevant info
            n += 1

if __name__ == '__main__':
    main()