#scrap Syndicat national de l'édition phonographique (SNEP) / 1994 - 2020 Top Albums

from bs4 import BeautifulSoup
import urllib.request
import csv
import pandas as pd
import time

topalbums = pd.DataFrame(columns=['year', 'rank', 'title', 'artist', 'editor'])

for year in range(1994, 2021) :
    url = 'https://snepmusique.com/les-tops/le-top-de-lannee/top-albums-annee/?annee={}'.format(year)
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    items = soup.find('div', attrs={'class': 'items'})
    results = items.find_all('div', attrs={'class': 'item'})
    last_rank = None
    
    for album in results:
        title = album.find('div', attrs={'class': 'titre'}).string
        artist = album.find('div', attrs={'class': 'artiste'}).string
        editor_temp = album.find('div', attrs={'class': 'editeur'}).string
        rank = album.find('div', attrs={'class': 'rang'}).string        
        if editor_temp != None:
            editor = editor_temp.rstrip()
        else :
            editor = None
            
        row = {
            'year' : year,
            'rank' : rank,
            'title' : title.rstrip(),
            'artist' : artist.rstrip(),
            'editor' : editor
        }
        
        topalbums = topalbums.append(row, ignore_index=True)
        last_rank = rank
        
    print('Scraping top {} albums for year {}'.format(last_rank, year))    
    time.sleep(1)
    
print('Scraping finished')
topalbums.to_csv('top-albums_1994-2020.csv', index=False)
