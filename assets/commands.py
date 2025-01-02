def tr_int(value: str, default = False):
    '''
    Переводит строку в число, если это возможно, в ином случае возвращает False или default, если он указан
    '''
    try:
        return int(value)
    except:
        return default