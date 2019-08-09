import requests
from bs4 import BeautifulSoup

from utils.utils import celphone_formatter


def fravega_scrap(path: str) -> list:
    """
    Scrapes the link provided, returning a list of dictionaries
    with the name and price of all the products in the webpage.

    Params:
    *path* the url provided to scrap 
    """
    fravega_articles = []
    done, counter = False, 1
    print("- Scraping Fravega ")
    while not done:
        new_path = path+f"?page={counter}" if counter!=1 else path
        r = requests.get(new_path)
        soup = BeautifulSoup(r.text, 'html.parser')
        if soup.find_all(string="No se han encontrado resultados"):
            done = True
        
        else:        
            for i in soup.find_all(attrs={"name": "item"}):
                price_to_format = i.find(attrs={"class": "price"}).text
                price = float(price_to_format.split('$')[1].replace(".", "").replace(",", "."))
                fravega_articles.append({
                    'name': celphone_formatter(i.find("h2").text),
                    'price': price
                })
            print(f'Scraping page: {counter}')
            counter+=1
    
    return fravega_articles
    