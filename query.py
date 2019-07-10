import requests, yaml
from bs4 import BeautifulSoup as bs
# Homemade Modules
import config, post
from smartdelay import delay

def do(configpath):
    configDict = config.get(configpath)

    with open('regions.yaml', 'r') as f:
        regions = yaml.safe_load(f)

    for city,nearbyArea in regions.items():
        if city in configDict['cities']:
            url_base = 'http://%s.craigslist.org/d/bicycles/search/bia%s' % (city, nearbyArea)
            params = dict(sort='date', srchType='T', hasPic=1, query=configDict['query'], max_price=configDict['max_price'], min_price=configDict['min_price'])
            headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
                       }
            rsp = requests.get(url=url_base, params=params, headers=headers)
            print("Fetching region: %s" % city)
            soup = bs(rsp.text, 'html.parser')
            print(rsp.url)
            for listing in soup.find_all('li', {'class': 'result-row'}):
                title = listing.find('p').find('a').text
                price = listing.find('span', {'class': 'result-price'}).text
                link = listing.find('a')['href']

                if post.check(link, configDict['titlekeywords'], configDict['bodykeywords'], configDict['framesizes'], configDict['min_frame'], configDict['max_frame']):
                    print('Listing: ', title, '\n', 'Price: ', price, '\n', link, '\n' * 2)
                delay(0.4, 100)

            delay(2, 100)
    print(configDict['titlekeywords'], configDict['bodykeywords'], configDict['framesizes'], configDict['min_frame'], configDict['max_frame'])