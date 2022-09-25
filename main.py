import requests
from bs4 import BeautifulSoup
import pandas as pd

from timeit import default_timer as timer

url = 'https://store.steampowered.com/search/results/?query&start=0&count=50&dynamic_data=&force_infinite=1&tags=19&snr=1_7_7_230_7&infinite=1'


# Total Results
def total_results(url):
    r = requests.get(url)
    data = dict(r.json())
    total_results = data['total_count']
    return int(total_results)


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
        title = game.find('span', {'class': 'title'}).text
        try:
            price = game.find('div', {'class': 'search_price'}).text.strip().split('£')[1]
        except:
            price = "Free game"
        try:
            discountedprice = game.find('div', {'class': 'search_price'}).text.strip().split('£')[2]
        except:
            discountedprice = price
        mygame = {
            'title': title,
            'price': price,
            'discountedPrice': discountedprice
        }
        gameslist.append(mygame)
    return gameslist


#  3. Output the Data csv
def output(gameslist):
    gamesdf = pd.concat([pd.DataFrame(g) for g in results])
    gamesdf.to_csv('gamesprices.csv', index=False)
    print("finished. Saved to csv")
    # print(gamesdf.head())
    return


results = []
for x in range(0, total_results(url), 50):
    data = get_data(
        f'https://store.steampowered.com/search/results/?query&start={x}&count=50&dynamic_data=&force_infinite=1&tags=19&snr=1_7_7_230_7&infinite=1')
    results.append(parse(data))
    print('Results Scraped: ', x)

output(results)

# print(total_results(url))
# data = get_data(url)
# gameslist = parse(data)
# output(gameslist)
