def make_df_from_xlsx(path):
    import pandas as pd
    from datetime import datetime, timedelta
    
    # считываем из excel
    data = pd.read_excel(path, header=5)

    # убираем пустые столбцы
    data.dropna(axis = 1, inplace = True)
    # убираем лишний столбец
    data.drop(['№'], axis = 1, inplace=True)
    # переименовываем столбцы
    data.columns = ['organisation', 'employee', 'birthday', 'position', 'division', 'status']
    # делаем стобец с ДР datetime
    data['birthday'] = pd.to_datetime(data['birthday'])

    # добавляем столбцы
    data['birthday_month'] = data['birthday'].apply(lambda x: x.month)                 # месяц
    data['birthday_day'] = data['birthday'].apply(lambda x: x.day)                     # день
    data['this_year_birthday'] = data['birthday'].apply(lambda x: x.strftime("%Y-%m-%d"))     # др в этом году
    data['this_year_birthday'] = data['this_year_birthday'].apply(lambda x: str(datetime.now().year) + x[4:]) 
    data['this_year_birthday'] = pd.to_datetime(data['this_year_birthday'])
    data['timedelta'] = data['this_year_birthday'] - datetime.today()                  # timedelta, для ближайшего ДР
    data['timedelta'] = data['timedelta'].apply(lambda x: x.days)

    return data

