import requests
import logging
from bs4 import BeautifulSoup
from minemeld.ft.basepoller import BasePollerFT

LOG = logging.getLogger(__name__)


class Miner(BasePollerFT):

  url = 'https://report.boonecountymo.org/mrcjava/servlet/SH01_MP.I00290s'
  response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
  html = response.content

  soup = BeautifulSoup(html)
  table = soup.find('tbody', attrs={'class': 'stripe'})

  for row in table.findAll('tr'):
    print row.prettify()
