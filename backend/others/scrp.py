import requests
from bs4 import BeautifulSoup


response1 = requests.get(
    url='https://en.wikipedia.org/wiki/List_of_chemical_elements', 
    # headers={'User-Agent': 'Mozilla/5.0'}
)

response2 = requests.get(
    url='https://sciencenotes.org/valences-of-the-elements/',
    headers={'User-Agent': 'Mozilla/5.0'}
)


# checking if the request was successful
if response1.status_code == 200 and response2.status_code == 200:
    
    soup1 = BeautifulSoup(response1.text, 'lxml')
    div = soup1.find('div', class_='mw-parser-output')
    table = div.find('table')
    head = table.find_all('thead')
    body1 = table.find('tbody', class_=None)
    target1 = body1.find_all('tr', class_='anchor')
# =============================================================
    soup2 = BeautifulSoup(response2.text, 'lxml')
    body2 = soup2.find('tbody', class_=None)
    target2 = body2.find_all('tr', class_=None)

    elements = []

    for row in target1:
        cells = row.find_all('td')
        
        data = [cell.get_text(strip=True) for cell in cells]
        
        element_data = {
            "atomic_num": data[0],
            "atomic_symbol": data[1],
            "name": data[2],
            "origin_of_name": data[3],
            "group": data[4],
            "period": data[5],
            "block": data[6],
            "atomic_mass": data[7],
            "density": data[8],
            "melt_point": data[9],
            "boil_point": data[10],
            "heat_capacity": data[11],
            "electronegativity": data[12],
            "natural_abundance": data[13],
            "origin": data[14],
            "phase": data[15]
        }

        elements.append(element_data)
    
    oxidation_states = []

    for row in target2:
        cells = row.find_all('td')
        
        data = [cell.get_text(strip=True) for cell in cells]
        oxidation_states.append(data[3])

    # first is garbage data
    oxidation_states.pop(0)
    # print(oxidation_states)
    for i, element in enumerate(elements):
        element['oxidation_states'] = oxidation_states[i].replace(" ", "")#.split(',')
        print(element['oxidation_states'])
    data = []
    for row in target2:
        cells = row.find_all('td')

        raw = [cell.find_all('strong') for cell in cells]
        data.append(raw[3])
    
    # first is garbage data    
    data.pop(0)
    valences = []
    for item in data:
        if len(item) == 0:
            valences.append(None)
            continue
        if len(item) > 1:
            element = [i.get_text() for i in item]
            valences.append(element)
            continue
        valences.append(item[0].get_text())

    valences[22] = valences[22].split(',') # only this static, cus anyway I retrive data from one site, so ...
    for i, element in enumerate(elements):
        element['valence'] = valences[i]
else:
    print('Failed to retrieve the webpage.')
# with open('some.py', 'w') as file:
#     file.write('elements = [')
#     for i in elements:
#         file.write(f"{i['atomic_symbol'], i['valence']},\n")
#     file.write(']')
# print(elements)

# with open('valences.py', 'w') as file:
#     data = [(i['atomic_symbol'],i['valence']) for i in elements]
#     file.write('elements = {\n')
#     for element in data:
#         file.write(f"'{element[0]}':{element[1]},\n")
#     file.write('}')
# import json
# with open("data.json", "w") as file:
#     json.dump(elements, file)
# print(elements)
