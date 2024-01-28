import requests
from bs4 import BeautifulSoup
import json


url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    vacancies = soup.find_all('div', {'class': 'vacancy-serp-item'})
    results = []
    for vacancy in vacancies:

        description = vacancy.find('div', {'class': 'g-user-content'}).text.lower()
        if 'django' in description and 'flask' in description:

            link = vacancy.find('a', {'class': 'bloko-link'}).get('href')
            salary = vacancy.find('div', {'class': 'vacancy-serp-item__compensation'}).text.strip()
            company = vacancy.find('div', {'class': 'vacancy-serp-item__meta-info'}).find('a').text.strip()
            city = vacancy.find('span', {'data-qa': 'vacancy-serp-item__location'}).text.strip()

            result = {
                'link': link,
                'salary': salary,
                'company': company,
                'city': city
            }
            results.append(result)

    with open('vacancies.json', 'w', encoding='utf-8') as file:
        json.dump(results, file, ensure_ascii=False, indent=4)

    print("Парсинг выполнен успешно и результаты сохранены в vacancies.json")
else:
    print("Ошибка при отправке запроса")

