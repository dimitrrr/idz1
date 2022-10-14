import requests
import textract
from bs4 import BeautifulSoup


def parse_url(link):
    html = requests.get(link).text
    soup = BeautifulSoup(html, "html.parser")
    res = soup.get_text()
    return res


def parse_file(filename):
    text = textract.process(filename)
    return text.decode('utf-8')
