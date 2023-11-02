from bs4 import BeautifulSoup
import requests
import pandas
import re

data = pandas.read_excel('demo.xlsx')


def get_year(text):
    year_match = re.search(f'Год выпуска:\s*(\d+)', text)
    print(year_match.group(1))
    return year_match.group(1)


def get_model_p(text):
    model_math = re.search(r'Модель: (.*)', text)
    print(model_math.group(1))
    return model_math.group(1)


def get_manufacture_div(text):
    match_manufacture = re.search('Производитель:\s*(\w+(?:\s+\w+)*)', text)
    return match_manufacture.group(1)


def get_model_div(text):
    match_model = re.search(r'Модель телефона:\s*(.+?)\s*(?:\.|Год)', text)
    print(match_model)
    return match_model.group(1)


def pars(link):
    response = requests.get(link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        model_tag_p = soup.find('p', class_='second-name')
        model_tag_div = soup.find('div', class_='desc_main')
        if model_tag_p:
            model = get_model_p(model_tag_p.text)
            manufacture = get_manufacture_div(model_tag_div.text)
            year = get_year(model_tag_div.text)
            print('=========')
        else:
            print(response.url)
            model = get_model_div(model_tag_div.text)
            manufacture = get_manufacture_div(model_tag_div.text)
            year = get_year(model_tag_div.text)
            print('=========')
        return manufacture, model, year

# 'https://mobihobby.ru/phone/lenovo_a606'
# 'desc_main'
# url = 'https://mobihobby.ru/phone/alcatel_3l__2021_'
# url_1 = 'https://mobihobby.ru/phone/lenovo_a606'
# url_2 = 'https://mobihobby.ru/phone/lenovo_s660'
# url_3 = 'https://mobihobby.ru/phone/philips_x516'
# pars(url)


data[['Производитель', 'Модель', 'Год']] = data['Ссылка'].apply(pars).apply(pandas.Series)
# data[['Модель 1', 'Год']] = data['Ссылка'].apply(pars).apply(pandas.Series)

data.to_excel('new_data.xlsx', index=False)

# pattern = r'Производитель:\s*(\w+)[^\w]+\s*Модель телефона:\s*(\w+)'
