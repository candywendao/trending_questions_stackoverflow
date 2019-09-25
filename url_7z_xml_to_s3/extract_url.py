'''This script parses the urls of data dump files and saves urls and file names in arrays.'''


from bs4 import BeautifulSoup
import requests


def extract_url(data_url):
    
    page = requests.get(data_url)
    soup = BeautifulSoup(page.text)
    file_names = []
    
    for link in soup.find_all('a'):
        if link.get('href')[-3:] == '.7z':
            file_names.append(link.get('href'))
    return file_names







