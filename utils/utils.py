from difflib import SequenceMatcher
import pandas as pd


def celphone_formatter(name: str) -> str:
    """
    Removes all unnecesary words from a string to
    keep it clean for further analysis and comparisons.

    Params:
    *name* the string to format 
    """
    name = name.replace("Celular", "").replace("Libre", "").replace("Liberado", "").replace("Celulares", "").replace("/", "").replace("  ", "")
    #strip colors
    name = name.replace("Negro", "").replace("Blanco", "").replace("Violeta", "").replace("Azul", "").replace("Azul Marino", "").replace("Gris", "").replace("Bronce", "")
    name = name.replace("Dorado", "").replace("Rosa", "").replace("NegroRojo", "").replace("NegroAzul", "").replace("Azul Marino", "").replace("Rojo", "")
    name = name.replace("Silver", "").replace("Gold", "").replace("Midnight", "").replace("Ceramic", "").replace("Blue", "").replace("Plata", "").replace("Grey", "")
    name = name.replace("Black", "").replace("Pink", "").replace("Deep Indigo", "").replace("Red", "").replace("Viva", "").replace("Marine", "").replace("Power", "")
    name = name.replace("Acero", "").replace("Violet", "").replace("Bronze", "")
    return(name.strip())


#def aire_acondicionado_formatter(name: str) -> str:
#    """
#    Removes all unnecesary words from a string to
#    keep it clean for further analysis and comparisons.
#
#    Params:
#    *name* the string to format 
#    """
#    name = name.replace("Aire", "").replace("Acondicionado", "").replace("Split", "").replace("Inverter", "").replace("Frío", "").replace("Calor", "").replace("Acond", "").replace("Portatil", "")
#    name = name.replace("Ventana", "").replace("Comercial", "").replace("Solo", "").replace("Frio", "").replace("Techo", "").replace("Frigorias", "").replace("/", "").replace(".", "").replace("  ", " ")
#    name = name.replace("para", "").replace("Wifi", "").strip()
#    return name 


def get_average_price(article_count: int, articles: list) -> float:
    """
    Gets the average price of a list of products

    Params:
    *article_count* number of articles 
    *articles* list of products
    """
    total_sum = sum([i['price'] for i in articles])
    average_price = round(total_sum/article_count, 2)
    return average_price


def matchmaker(element: dict, dictionary: list) -> dict:
    """
    Compares the price of an dictionary, to every item of a list
    if the comparison get more than 95% of compatibility between
    the strings, it returns the element.

    Params:
    *element* the dictionary to compare the list with.
    *dictionary* the list of dictionaries with names and prices.
    """
    for l in dictionary:
        if (SequenceMatcher(None, l['name'], element['name']).ratio()*100)> 95.0:
            return l
    else:
        return None


def data_to_excel(df_garbarino: pd.DataFrame, df_fravega: pd.DataFrame, 
    df_matches: pd.DataFrame, df_stats: pd.DataFrame) -> None:
    """
    Exports the analized dataframes to excel, including a chart
    with the results

    Params:
    *df_garbarino* Dataframe with Garbarino products.
    *df_fravega* Dataframe with Fravega products.
    *df_matches* Dataframe with matches between products.
    *df_stats* Dataframe with statistics.
    """
    print("- Exporting Data to Excel")
    writer = pd.ExcelWriter('ouput.xlsx',engine='xlsxwriter')

    df_garbarino.to_excel(writer, sheet_name='Garbarino Products', index=False)
    df_fravega.to_excel(writer, sheet_name='Fravega Products', index=False)
    
    df_matches.to_excel(writer, sheet_name='Output')
    stats_start = len(df_matches)+4
    df_stats.to_excel(writer, sheet_name='Output', startrow=stats_start)
    workbook = writer.book
    worksheet = writer.sheets['Output']
    worksheet.set_column('A:A', 25)
    worksheet.set_column('B:B', 15)
    worksheet.set_column('C:C', 15)
    chart = workbook.add_chart({'type': 'column'})

    series_max_row = len(df_matches)+1

    chart.add_series({
        "values": f"=Output!$B$2:$B${series_max_row}",
        "fill": {'color': 'red'},
        "name": f"Garbarino",
        "categories": f"=Output!$A$2:$A${series_max_row}"
        })
    chart.add_series({
        "values": f"=Output!$C$2:$C${series_max_row}",
        "fill": {'color': 'blue'},
        "name": f"Fravega",
        "categories": f"=Output!$A$2:$A${series_max_row}"
        })

    chart.set_title({'name': 'Cell Phone Price Comparison Between Fravega and Garbarino in ARS'})
    chart.set_size({'width': 720, 'height': 526})
    worksheet.insert_chart('F2', chart)
    writer.save()
