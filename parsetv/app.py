import requests
import json
from config import key, shows


searching = False
lookup = "omdbid"  # omdbid
show_type = "series"

for show in shows:
    if searching:
        url = f"http://www.omdbapi.com/?s={show}&apikey={key}&type=series"
        response = requests.get(url)
        c = json.loads(response.content)

        if 'Error' in c:
            if "Series not found!" in c["Error"]:
                print(show, c['Error'])
                continue
            if 'Request limit reached!' in c["Error"]:
                print("LIMIT REACHED")
                break

        search = c.get("Search", [])
        title = search[0].get('Title', '')
        imdbid = search[0].get('imdbID', '-1')
        show_type = search[0].get('Type', '')
        year = search[0].get('Year', '')
        print(f'"{title}","{imdbid}","{show_type}","{year}"')
        a = 1
    else:
        # Looking for an exact match
        if lookup == "title":
            # Title
            url = f"http://www.omdbapi.com/?t={show}&apikey={key}&type={show_type}"
        else:
            # ID
            url = f"http://www.omdbapi.com/?i={show}&apikey={key}&type={show_type}"

        response = requests.get(url)
        c = json.loads(response.content)
        if 'Error' in c:
            if "Series not found!" in c["Error"]:
                print(show, c['Error'])
                continue
            if 'Request limit reached!' in c["Error"]:
                print("LIMIT REACHED")
                break
        seasons = c.get('totalSeasons', -1)
        title = c.get('Title', '')
        imdbid = c.get('imdbID', '-1')
        show_type = c.get('Type', '')
        year = c.get('Year', '')

        if show_type == "movie":
            print(f'"{title}","{imdbid}","{show_type}","{year}"')
        if show_type == "series":
            episodes_count = 0
            if str(seasons).isnumeric():
                seasons = int(seasons)
            else:
                seasons = 1
            for season in range(1, seasons + 1):
                url2 = f"http://www.omdbapi.com/?Season={season}&i={imdbid}&apikey={key}"
                response2 = requests.get(url2)
                c2 = json.loads(response2.content)
                episodes = c2.get("Episodes", [])
                episodes_count += len(episodes)
                a = 1
            print(f'"{title}","{imdbid}","{show_type}","{year}","{episodes_count}"')
print("DONE")
