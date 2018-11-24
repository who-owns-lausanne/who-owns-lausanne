import bs4
import os

DATA_DIR = 'data/anibis/listings/'
for listing_file in os.listdir(DATA_DIR):
    with open(DATA_DIR + listing_file) as html:
        soup = bs4.BeautifulSoup(html, features='lxml')
        for listing in soup.find_all('a', class_ = 'listing-title'):
            print(listing['href'])
