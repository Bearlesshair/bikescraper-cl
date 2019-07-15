import requests, yaml, progressbar, json, os
from bs4 import BeautifulSoup as bs
# Homemade Modules
import post, getchanged
from smartdelay import delay


def do(configDict):
    with open('regions.yaml', 'r') as f:
        regions = yaml.safe_load(f)

    total = []
    for city, nearbyArea in regions.items():
        if city in configDict['cities']:
            params = dict(sort='date', hasPic=1, query=configDict['query'], max_price=configDict['max_price'],
                          min_price=configDict['min_price'], s=0)
            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
            }

            while True:
                # set up request
                url_base = 'http://%s.craigslist.org/d/bicycles/search/bia%s' % (city, nearbyArea)
                # srchType='T'
                # make search request and parse with beautiful soup
                print("Fetching region: %s" % city)
                while True:
                    try:
                        rsp = requests.get(url=url_base, params=params, headers=headers)
                    except (ConnectionError, requests.exceptions.RequestException) as e:
                        print("\nConnection error, pausing requests ~5s...")
                        delay(5, 10)
                        continue
                    break
                soup = bs(rsp.text, 'html.parser')
                print(rsp.url)
                for listing in soup.find_all('li', {'class': 'result-row'}):
                    title = listing.find('p').find('a').text
                    price = listing.find('span', {'class': 'result-price'}).text
                    link = listing.find('a')['href']
                    total.append(dict(Listing=title, Price=price, Link=link, Region=city.title()))
                delay(2, 100)
                if soup.find('a', {'class': 'button next'})['href'] == '':
                    break
                params['s'] += 120

    jsonname = os.path.join(os.path.expanduser("~"), '.bikescraper-cl', 'total.json')
    changed = getchanged.compare(total, jsonname)

    # save total to JSON
    with open(jsonname, 'w') as json_file:
        json.dump(total, json_file)

    # check individual postings for each region
    relevant = []
    if changed == []:
        print("No new listings.")
    else:
        print("Checking posts...")
        for listing in progressbar.progressbar(changed):
            if post.check(listing['Link'], configDict['titlekeywords'], configDict['bodykeywords'], configDict['framesizes'],
                          configDict['min_frame'], configDict['max_frame']):
                relevant.append(listing)
            delay(0.4, 100)

    print("Completed query for: ", configDict['titlekeywords'], configDict['bodykeywords'], configDict['framesizes'], configDict['min_frame'], configDict['max_frame'])

    return relevant