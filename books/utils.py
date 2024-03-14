
def clean_string(input_str:str) -> str:
    """ 
    Функция убирает лишние пробелы из строки 
    и заменяет лишние символы, 
    возвращает очищенную строку
    """
    
    # удаление лишних пробелов
    lst = input_str.split() # список из слов
    formatted_str = ' '.join(lst) # строка без лишних пробелов
    
    # удаление кавычек "" и дефисов --
    if '\"' in formatted_str:
        print('кавычки есть')
        formatted_str.replace("\"", "\''")
        
    # TODO: дефисы не заменяются на другие символы в строке
    # if '--' in formatted_str:
    #     print('дефисы есть')
    #     formatted_str.replace("--", ", ")
        
    return formatted_str

def divide_authors(lst:list) -> list:
    
    """ 
    Функция проверяет нахождение слова 'with' в элементе списка,
    разбивает строку на две составляющих, 
    возвращает список с 2 строками без пробелов
    """
    
    for item in lst:
        if 'with'in item:
            author_1, author_2 = item.split(' with ')
            lst.append(author_1.strip())
            lst.append(author_2.strip())
            lst.remove(item)
            
            return lst
        
def clean_list(lst: list) -> list:
    
    """ 
    Функция удаляет из списка пустые элементы, в списках где больше одного элемента 
    возвращает список без пустых элементов
    """
    
    # result = [lst.remove(item) for item in lst if len(item) == 0]
    if len(lst):
        for item in lst:
            if len(item) == 0:
                lst.remove(item)
    return lst

def is_correct_isbn(number:int) -> bool:
    pass

def get_useful_date_format(date:str) -> str:
    # "2010-06-01T00:00:00.000-0700" -> "2010-06-01"
    
    """ 
    Функция изменяет формат даты и оставляет только дату без времени
    возвращает строку с датой
    """
    
    import datetime as dt

    date = dt.datetime.strptime(date, "%Y-%m-%dT%I:%M:%S-%f")
    # date = dt.datetime.strptime(date, "%d.%m.%Y")

    new_date = date.strftime("%Y-%m-%d")
    return new_date

# ! анализ books.json
