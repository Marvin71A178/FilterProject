import requests
from bs4 import BeautifulSoup

url = "https://old.accupass.com/search/r/0/0/0/0/4/300/00010101/99991231"

# send a GET request to the website and retrieve the HTML content
response = requests.get(url)
html_content = response.content

# parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# find all the events on the page
events = soup.find_all("div", class_="search_unit")

print(soup)
