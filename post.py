import requests
from bs4 import BeautifulSoup as bs
from smartdelay import delay

def frameFits(soup, framesizes, min_frame, max_frame):
    # allow for passing when min_frame or max_frame are None
    if min_frame is None:
        min_frame = 0
    if max_frame is None:
        max_frame = 999
    framesizes = [x.lower() for x in framesizes]

    # extract frame size
    attributes = soup.find('p', {'class': 'attrgroup'})
    for attr in attributes.find_all('span'):
        if "frame size: " in attr.text:
            frameSize = attr.text[12:].lower()
            if frameSize in framesizes:     # case for if frame size is words and contained in valid frame size list
                return True
            else:
                try:
                    frameFloat = float(frameSize)
                    if frameFloat >= min_frame and frameFloat <= max_frame:
                        return True     # frame size is float and within range
                    else:
                        return False       # frame size is float and outside range
                except:
                    return False    # Frame size IS words but not contained in framesizes list
    return True     # no frame size attribute, will not exclude post

def checkTitle(soup, titlekeywords):
    title = soup.find('span', {'id': 'titletextonly'}).text
    for word in titlekeywords:
        if word.lower() not in title.lower():
            return False
    return True

def checkBody(soup, bodykeywords):
    body = soup.find('section', {'class':'userbody'}).text
    for word in bodykeywords:
        if word.lower() not in body.lower():
            return False        # if keyword missing from body return false
    return True     # otherwise return true

def check(url, titlekeywords, bodykeywords, framesizes, min_frame, max_frame):
    # fetch posting
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

    while True:
        try:
            rsp = requests.get(url=url, headers=headers)
        except (ConnectionError, requests.exceptions.RequestException) as e:
            print("Connection error, pausing requests ~5s...")
            delay(5, 10)
            continue
        break

    soup = bs(rsp.text, 'html.parser')

    # TODO Add AND and OR functionality - Currently is AND
    # check if passes all criteria, pass true by default
    valid = True
    if framesizes is not None or min_frame is not None or max_frame is not None:
        valid *= frameFits(soup, framesizes, min_frame, max_frame)
    if titlekeywords is not None:
        valid *= checkTitle(soup, titlekeywords)
    if bodykeywords is not None:
        valid *= checkBody(soup, bodykeywords)
    return valid