import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

url = 'https://store.steampowered.com/search/results/?query&start=0&count=50&dynamic_data=&force_infinite=1&tags=19&snr=1_7_7_230_7&infinite=1'


#  1. Get the data
def get_data(url):
    r = requests.get(url)
    data = dict(r.json())
    return data['results_html']

#  2. Parse the data
def parse(data):
    gameslist = []
    soup = BeautifulSoup(data, 'html.parser')
    games = soup.find_all('a')
    for game in games:
        title = game.find('span', {'class' : 'title'}).text
        try:
            price = game.find('div', {'class': 'search_price'}).text.strip().split('£')[1]
        except: price = "Free game"
        try:
            discountedPrice = game.find('div', {'class': 'search_price'}).text.strip().split('£')[2]
        except:
            discountedPrice = price
        mygame = {
            'title': title,
            'price': price,
            'discountedPrice' : discountedPrice
        }
        gameslist.append(mygame)
    return gameslist

#  3. Output the Data csv
def output(gameslist):
    gamesdf = pd.DataFrame(gameslist)
    gamesdf.to_csv('gamesprices.csv', index=False)
    print("finshed. Saved to csv")
    return


data = get_data(url)
gameslist = parse(data)
output(gameslist)

