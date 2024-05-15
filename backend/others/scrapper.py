import requests
from bs4 import BeautifulSoup
import re

url = "https://simple.wikipedia.org/wiki/Periodic_table"

response = requests.get(url)


"""

name, 
atomic_num, 
atomic_symbol, 
atomic_mass, 
valence, 
electron_conf, 
isotopes, 
per_table_group, 
per_table_period, 
metallicity, 
chem_react, 
ionization_energy, 
electronegativity, 
melt_point, 
boil_point, 
density, 
oxidation_states, 
radioactive_prop, 
natural_abundance

"""


print("({})".format(response.status_code))
# Check if the request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'lxml')
# ==========================================
    # body = soup.find("body", class_="skin-vector skin-vector-search-vue mediawiki ltr sitedir-ltr mw-hide-empty-elt ns-0 ns-subject mw-editable page-Periodic_table rootpage-Periodic_table skin-vector-2022 action-view uls-dialog-sticky-hide vector-below-page-title")
    # # print(body)
    # root_div = body.find('div', class_='mw-page-container')
    # outter_div = root_div.find('div', class_='mw-page-container-inner')
    # inner_div = outter_div.find('div', class_='mw-content-container')
    # main = inner_div.find('main', class_='mw-body')
    # div1 = main.find('div', class_='vector-body ve-init-mw-desktopArticleTarget-targetContainer')
    # div2 = div1.find('div', class_='mw-body-content mw-content-ltr')
    # target_div = div2.find('div', class_='mw-parser-output')

    # table = target_div.find('table', class_=None)
    # tbody = table.find('tbody')
# ==========================================

    table = soup.find('table', class_=None).text
    # print(table)
    pattern = r'(\d+)([A-Za-z]+)'
    elements = re.findall(pattern, table)
    # new_elements = [int(i[0]) for i in elements]
    print(elements)
else:
    print('Failed to retrieve the webpage.')
