import json
import requests


# функция для парсинга данных по ссылке 
def parse_json_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        json_data = response.json()
        print(type(json_data))
        print('Данные загружены')
    except requests.RequestException as e:
        print(f"Проблема с выполнением HTTP-запроса: {e}")
    except json.JSONDecodeError:
        print("Не удалось декодировать JSON. Пожалуйста, попробуйте еще раз.")
        
    return json_data


