import requests
from bs4 import BeautifulSoup
from pprint import pprint

url = "https://index.minfin.com.ua/ua/russian-invading/casualties/"

response = requests.get(url)
soup = BeautifulSoup(response.text, "lxml")

quotes = soup.find_all('div', class_ = 'ajaxmonth')

first_div = soup.find('div')

first_link = first_div.find('a')

# print(first_link.get_text().strip())
# print(first_link.children)
print(quotes)
# print(soup.select('.text'))
