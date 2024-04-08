import datetime
import json

from typing import List
import requests


DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%f%z'
DATE_TYPE_NAME = '$date'
DATE_OBJ_KEYS = [DATE_TYPE_NAME]


def decode_dates(obj):
    """
    Функция проверяет ключи в словаре на соответствие формату,
    парсит дату и изменяет ее согласно формату,
    возвращает дату в удобном формате
    """

    if list(obj.keys()) == DATE_OBJ_KEYS:
        return datetime.datetime.strptime(
            obj[DATE_TYPE_NAME], DATE_FORMAT).date()
    else:
        return obj


def str_to_json(json_str: str):
    """
    Функция преобразовывает строку в формат json
    возвращает
    """

    return json.loads(json_str, object_hook=decode_dates)


def parse_json_from_url(url) -> List[dict]:

    """
    Функция парсит данные по ссылке url
    возвращает данные в виде списка
    """

    try:
        response = requests.get(url)
        response.raise_for_status()
        response_text = response.text
        json_data = str_to_json(response_text)

        # TODO: добавить логику при невозможности загрузки по сети
    except requests.RequestException as e:
        print(f"Проблема с выполнением HTTP-запроса: {e}")
    except json.JSONDecodeError:
        print("Не удалось декодировать JSON. Пожалуйста, попробуйте еще раз.")

    return json_data
