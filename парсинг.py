import requests
from bs4 import BeautifulSoup
import csv

# Обозначаем заголовки
headers = {
    'Accept': "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}

# Создаем переменную с ссылкой на страницу которую будем парсить
url = 'https://vladivostok.drom.ru/toyota/all/?distance=1000&maxprice=300000&transmission[]=2&transmission[]=3&transmission[]=4&transmission[]=5&transmission[]=-1&ph=1&pts=2&damaged=2&unsold=1&isOwnerSells=1'

# Дополнительно обозначаем "базовый" url - нам это пригодиться в будущем
base_url = 'https://vladivostok.drom.ru/toyota/all/'

# Используем метод ".get" библиотеки "requests" - для выгрузки кода страницы
response = requests.get(url, headers=headers)

# Структурируем выгруженный код для читабельности
soup = BeautifulSoup(response.text, 'lxml')

# Создаем список - пригодится далее
cars = []

# Создаем цикл в котором будем перебирать нужные нам значения страницы
while True:

    # Здесь мы выделяем кол-во страниц по которым пройдемся кодом
    for page in range(1, 11):
        next_page_url = f"{base_url}page{page}/?distance=1000&maxprice=300000&transmission[]=2&transmission[]=3&transmission[]=4&transmission[]=5&transmission[]=-1&ph=1&pts=2&damaged=2&unsold=1&isOwnerSells=1"
        response = requests.get(next_page_url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')

        # Здесь мы вделяем блокис информацией, а также какие миенно данные мы будем искать
        for car_block in soup.find_all(class_='css-xb5nz8 e1huvdhj1'):
            car_title = car_block.find(class_='css-l1wt7n e3f4v4l2')
            car_price = car_block.find('div', {'class': 'css-1dv8s3l eyvqki91'}).find('span', {'data-ftid': 'bull_price'})
            car_description = car_block.find_all('span',{'data-ftid': 'bull_description-item'})

            # Далее записываем текстовые значения и раставляем заглушки
            if car_title is not None:
                car_title = car_title.text.strip()
            else:
                car_title = 'N/A'

            if car_price is not None:
                car_price = car_price.text.strip()
            else:
                car_price = 'N/A'

            # Здесь интересная ситуация, т.к. на сайте эти значения имеют один класс, то при записи мы берем только первое
            # значение, выход - записывать все значения в список
            if car_description is not None:
                car_description_list = [item.text.strip() for item in car_description]
            else:
                car_description_list = ['N/A']
            # Записываем значения в ранее созданный список
            cars.append({'Назвние': car_title, 'Цена': car_price, 'Описание': car_description_list})
    else:
        break

# В самом коде страницы пробелы имеют специфическое обозначение, которые код ниже заменяет на пробел
for price in cars:
    price['Цена'] = price['Цена'].replace('\xa0', ' ')
print(cars)

# Ну а получившийся результат мы записываем в csv-файл
# ("w" - режим записи, "utf-8" - кодировка, "newline" - разделитель строк

with open('cars.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Назвние', 'Цена', 'Описание'])
    for car in cars:
        writer.writerow([car['Назвние'], car['Цена'], ','.join(car['Описание'])])
