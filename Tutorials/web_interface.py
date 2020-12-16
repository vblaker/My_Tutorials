import random
import urllib.request
from urllib import request
import re


def download_web_image(url):
    name = random.randrange(1, 1000)
    full_name = str(name) + ".jpg"
    urllib.request.urlretrieve(url, full_name)

# download_web_image('http://i2.cdn.cnn.com/cnnnext/dam/assets/160303091353-trump-romney-split-medium-tease.jpg')


goog_ticker_url = 'http://chart.finance.yahoo.com/table.csv?s=GOOG&a=9&b=18&c=2016&d=10&e=18&f=2016&g=d&ignore=.csv'


def download_stock_data(csv_url):
    response = request.urlopen(csv_url)
    csv_raw = response.read()
    csv_str = str(csv_raw)
    lines = csv_str.split("\\n")
    dest_url = r'goog.csv'
    fx = open(dest_url, "w")
    for line in lines:
        fx.write(line + "\n'")
    fx.close()


download_stock_data(goog_ticker_url)


# connect to a URL
url = 'http://python.org/'
# website = urllib.request.urlopen(url)

# read html code
with urllib.request.urlopen('http://www.python.org/') as response:
    html_page_raw = response.read()
    html_page_str = str(html_page_raw)

# use re.findall to get all the links
fp = open(r'links.html', "w")
fp.write(html_page_str)
fp.close()
#print(html_page_str)
links = re.findall('"((http|ftp)s?://.*?)"', html_page_str)
print(links)
print("I found %d links on that page!" % len(links))
