import random
import time
import requests
from itertools import cycle
import cianparser

# Список прокси-серверов
proxies = [
    "http://27.112.70.155",
    "http://43.134.32.184",
    "http://43.134.68.153",
    "http://41.204.63.118"
]

# Цикл для прокси
proxy_pool = cycle(proxies)

# Инициализация парсера для Москвы
moscow_parser = cianparser.CianParser(location="Королев")

# Функция для выполнения запроса с использованием текущего прокси
def make_request_with_proxy(url):
    proxy = next(proxy_pool)
    print(f"Используем прокси: {proxy}")
    try:
        response = requests.get(url, proxies={"http": proxy, "https": proxy})
        print(f"Статус ответа: {response.status_code}")
        return response
    except requests.exceptions.ProxyError:
        print("Ошибка при подключении к прокси.")

# Начало сбора данных
data = moscow_parser.get_flats(
    deal_type="sale",
    rooms=(1, 2, 3, 4),
    with_saving_csv=True,
    with_extra_data=True,
    additional_settings={
        "start_page": 1,
        "end_page": 100000
    }
)

# Добавление случайной задержки между запросами и использование прокси
for page in range(1, 100000):
    time.sleep(random.uniform(1, 5))  # Случайная задержка от 1 до 5 секунд
    # Вызов парсинга следующей страницы с использованием текущего прокси
    url = f"https://cian.ru/cat.php?deal_type=sale&region=1&currency=2&object_type[0]=1&p={page}"
    response = make_request_with_proxy(url)
    # Проверка ответа и дальнейшая обработка данных
    if response and response.status_code == 200:
        # Обработка данных страницы
        print(f"Данные страницы {page} получены")
    else:
        print(f"Не удалось получить данные для страницы {page}")