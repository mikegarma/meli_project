import pandas as pd

from scrapers.fravega import fravega_scrap
from scrapers.garbarino import garbarino_scrap
from utils.utils import matchmaker, data_to_excel, get_average_price


product_name = "Celulares"

#Defining urls
fravega_path = "https://www.fravega.com/l/celulares/celulares-liberados/"
garbarino_path = "https://www.garbarino.com/productos/celulares-libres/4359"

#Scraping
fravega_articles = fravega_scrap(fravega_path)
garbarino_articles = garbarino_scrap(garbarino_path)

#Matchmaking between products
matches = []
for article in garbarino_articles:
    match = matchmaker(article, fravega_articles)
    if match:
        matches.append({
            'name':article['name'],
            'garbarino_price': article['price'],
            'fravega_price': match['price']
        })

#Getting stats
count_fravega_articles = len(fravega_articles)
average_price_fravega = get_average_price(count_fravega_articles, fravega_articles)

count_garbarino_articles = len(garbarino_articles)
average_price_garbarino = get_average_price(count_garbarino_articles, garbarino_articles)

stats = [
    {
        'stat': 'Product Quantity',
        'Fravega': len(fravega_articles),
        'Garbarino': len(garbarino_articles)
    },
    {
        'stat': 'Average Product Price',
        'Fravega': average_price_fravega,
        'Garbarino': average_price_garbarino,
    },
]

#Compiling data in Dataframes
df_stats = pd.DataFrame(stats).set_index('stat')
df_garbarino = pd.DataFrame(garbarino_articles)
df_fravega = pd.DataFrame(fravega_articles)
df_matches = pd.DataFrame(matches).set_index('name')

#Exporting data to an excel file
data_to_excel(df_garbarino, df_fravega, df_matches, df_stats)

print("- Process completed successfully, please check the excel output.")
