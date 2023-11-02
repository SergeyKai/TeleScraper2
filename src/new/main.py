from bs4 import BeautifulSoup
import requests
import pandas
import re

data = pandas.read_excel('demo.xlsx')

"""
1800 Мгц (8-ядерный), граф.процессор

64 Гб + 512 Гб, 4 Гб RAM, microSDXC, microSDHC
100 Мб + 4 Гб, microSD
80 Мб + 8 Гб, microSDHC, microSD, горячая замена
"""


def get_corrent_CP(text: str):
    if text == 'Нет информации':
        return (text, text)
    if '(' in text:
        cp_cores = text.split('-')[0][-1]
        corrent_MZ = text.split()[0]
        return (corrent_MZ, cp_cores)
    else:
        corrent_MZ = text.split()[0]
        return (corrent_MZ, "Нет информации")


"""
1800 Мгц (8-ядерный), граф.процессор

64 Гб + 512 Гб, 4 Гб RAM, microSDXC, microSDHC
100 Мб + 4 Гб, microSD
80 Мб + 8 Гб, microSDHC, microSD, горячая замена
32 Гб, 2 Гб RAM
512 Мб + 32 Гб, 512 Мб RAM, microSDHC, microSD
   0             1          2           3               4               5
['Память', 'add_storage', 'ram', 'storage_type1', 'storage_type2', 'горячая замена']
"""


def get_data_storage(text: str):
    storage_list = text.split(',')
    current_data = [0, 0, 0, 0, 0, 0]
    count = 0
    for i in storage_list:
        if '+' in i:
            current_data[0], current_data[1] = i.split('+')
        elif 'RAM' in i:
            current_data[2] = i
        elif 'горячая замена' in i:
            current_data[5] = 1
        else:
            if current_data[3] == 0:
                current_data[3] = i
            else:
                current_data[4] = i
    return current_data

    # if len(storage_list) == 4:
    #     storage = storage_list[0].split('+')[0].strip()
    #     add_storage = storage_list[0].split('+')[-1].strip()
    #     ram = storage_list[1]
    #     storage_type1 = storage_list[-1]
    #     storage_type2 = storage_list[-2]
    #     current_data[0] = storage
    #     current_data[1] = add_storage
    #     current_data[2] = ram
    #     current_data[3] = storage_type1
    #     current_data[3] = storage_type2


# data[['Процессор', 'cp_cores']] = data['Процессор'].apply(get_corrent_CP).apply(pandas.Series)

data[['Память', 'add_storage', 'ram', 'storage_type1', 'storage_type2', 'горячая замена']] = data['Память'].apply(
    get_corrent_CP).apply(pandas.Series)

# get_data_storage('64 Гб + 512 Гб, 4 Гб RAM, microSDXC, microSDHC')

data.to_excel('new_data.xlsx', index=False)
