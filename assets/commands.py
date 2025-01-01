def tr_int(value: str):
    '''
    Переводит строку в число, если это возможно, в ином случае возвращает False
    '''
    try:
        return int(value)
    except:
        return False