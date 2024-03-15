
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
    
    if len(lst) > 1:
        return list(filter(None, lst))
    return lst

def is_correct_isbn(number:int) -> bool:
    
    """ 
    Функция проверяет если в isbn все символы цифры
    возвращает True/False
    """
    
    try:
        nums = int(number)
        # TODO: можно проверить код isbn на корректность составления
        return True
    except Exception as e:
        return False
    
def clean_date_format(date:str) -> str:
    
    """ 
    Функция изменяет формат даты и оставляет только дату без времени
    возвращает строку с датой
    """
    
    date_lst = date.split('T')[0]
    return ''.join(date_lst)

