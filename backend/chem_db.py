import psycopg2 as pg

try:
    conn = pg.connect(
        host="__",
        database="chemstore",
        port=5432,
        user="__",
        password="__"
    )
    cursor = conn.cursor()
    print("connection established\n")
except Exception as err:
    print("something went wrong\n", err)

def fetch_data():
    cursor.execute('''SELECT * FROM elements''')
    data = cursor.fetchall()
    return data

def create_entry():
    cursor.execute('''INSERT INTO players (id, name, age) 
                    VALUES (%s, %s, %s)''', (4, 'My Ex', 22))

    add_data = cursor.fetchone()
    conn.commit()
    return add_data


def create_table():
    cursor.execute('''
                    CREATE TABLE Elements (
                        atomic_num integer not null,
                        atomic_symbol varchar(2) not null,
                        name varchar() not null,
                        origin_of_name text not null,
                        group_of text not null,
                        period text not null,
                        block varchar(7) not null,
                        atomic_mass decimal not null,
                        density decimal not null,
                        melt_point decimal not null,
                        boil_point decimal not null,
                        heat_capacity decimal not null,
                        electronegativity decimal not null,
                        natural_abundance decimal not null,
                        origin text not null,
                        phase text not null,
                        oxidation_states varchar(30) not null,
                        valence integer not null
                    );
                   ''')
    add_data = cursor.fetchone()
    conn.commit()
    return add_data

# some = {
#     "atomic_num": "1", 
#     "atomic_symbol": "H", 
#     "name": "Hydrogen", 
#     "origin_of_name": "Greekelementshydro-and-gen, 'water-forming'", 
#     "group_of": "1", 
#     "period": "1", 
#     "block": "s-block", 
#     "atomic_mass": "1.0080", 
#     "density": "0.00008988", 
#     "melt_point": "14.01", 
#     "boil_point": "20.28", 
#     "heat_capacity": "14.304", 
#     "electronegativity": "2.20", 
#     "natural_abundance": "1400", 
#     "origin": "primordial", 
#     "phase": "gas", 
#     "oxidation_states": ["1", " 0", " -1"], 
#     "valence": "1"
# }
# """
# 	atomic_num integer not null,
# 	atomic_symbol varchar(2) not null,
# 	name varchar() not null,
# 	origin_of_name text not null,
# 	group_of text not null,
# 	period text not null,
# 	block varchar(7) not null,
# 	atomic_mass decimal not null,
# 	density decimal not null,
# 	melt_point decimal not null,
# 	boil_point decimal not null,
# 	heat_capacity decimal not null,
# 	electronegativity decimal not null,
# 	natural_abundance decimal not null,
# 	origin text not null,
# 	phase text not null,
# 	oxidation_states varchar(30) not null,
# 	valence integer not null
# """
# {'atomic_num': '79', 
#  'atomic_symbol': 'Au', 
#  'name': 'Gold', 
#  'origin_of_name': "English, from the same Proto-Indo-European root as 'yellow'·Symbol Au is derived from Latinaurum", 
#  'group': '11', 
#  'period': '6', 
#  'block': 'd-block', 
#  'atomic_mass': '196.97', 
#  'density': '19.3', 
#  'melt_point': '1337.33', 
#  'boil_point': '3129', 
#  'heat_capacity': '0.129', 
#  'electronegativity': '2.54', 
#  'natural_abundance': '0.004', 
#  'origin': 'primordial', 
#  'phase': 'solid', 
#  'oxidation_states': "7,5,3,2,1,0,-1", 
#  'valence': '3'}
