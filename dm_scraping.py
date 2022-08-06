import requests
from bs4 import BeautifulSoup

url = "https://projects.the-examples-book.com/companies/"
reqs = requests.get(url)
soup = BeautifulSoup(reqs.text, 'html.parser')
 
url_dict = {}
for link in soup.find_all('a'):
    url_name = "https://projects.the-examples-book.com" + link.get('href')
    #print(url_name)
    url_dict[url_name] = []

for url_name in url_dict:
    reqs = requests.get(url_name)
    soup = BeautifulSoup(reqs.text, 'html.parser')
 
    for sub_url in soup.find_all('a'):
        sub_url_name = "https://projects.the-examples-book.com" + sub_url.get('href')
        url_dict[url_name].append(sub_url_name)

print(url_dict)
