import requests
from bs4 import BeautifulSoup

from utils.utils import celphone_formatter


def garbarino_scrap(path: str) -> dict:
    garbarino_articles = []
    done, counter = False, 1
    print("- Scraping Garbarino ")
    while not done:
        new_path = path+f"?page={counter}" if counter!=1 else path
        r = requests.get(new_path)
        soup = BeautifulSoup(r.text, 'html.parser')
        if soup.find_all(string="No hay resultados para esta búsqueda"):
            done = True
        
        else:        
            for i in soup.find_all(attrs={"class": "itemBox"}):
                price_to_format = i.find(attrs={"class": "value-item"}).text
                price = float(price_to_format.split('$')[1].replace(".", "").replace(",", "."))
                garbarino_articles.append({
                    'name': celphone_formatter(i.find("h3").text),
                    'price': price
                })
            print(f'Scraping page: {counter}')
            counter+=1
    
    return garbarino_articles
