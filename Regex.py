# --------------------------------------------------
# This file contains functions using regular expressions
#
# (C) 2020 Esipov Paul
# Distributed under GNU public license
# email: esipov.p@mail.ru
# --------------------------------------------------
# Move to EventClass.py class
import re
import datetime
ru_months = [
    'января', 'февраля', 'марта',
    'апреля', 'мая', 'июня',
    'июля', 'августа', 'сентября',
    'октября', 'ноября', 'декабря'
]
date_regex_options = {
    'today': r'сегодня в (\d{2}):(\d{2})',
    'tomorrow': r'завтра в (\d{2}):(\d{2})',
    'other_year': r'(\d{0,2}) (\w+) (\d{2,4}) г\. в (\d{2}):(\d{2})',
    'this_year': r'(\d{1,2}) (\w+) в (\d{2}):(\d{2})'
}


# Move to EventClass.py class
def get_std_time_str(time_str):
    """ Build the  datetime string that is readable by MySql server

    :param time_str:
    :return: mysql datetime string
    """
    for key in date_regex_options:
        pattern = re.compile(date_regex_options[key])
        match_res = pattern.findall(time_str)
        if match_res:
            print(f'key        = {key}')
            if key is 'today':
                cur_dt = datetime.datetime.now()
                return f'{str(cur_dt.year)}-' \
                       f'{str(cur_dt.month).zfill(2)}-' \
                       f'{str(cur_dt.day).zfill(2)} ' \
                       f'{str(match_res[0][0]).zfill(2)}:' \
                       f'{str(match_res[0][1]).zfill(2)}:00'

            elif key is 'tomorrow':
                cur_dt = datetime.datetime.now()
                return f'{str(cur_dt.year)}-' \
                       f'{str(cur_dt.month).zfill(2)}-' \
                       f'{str(cur_dt.day + 1).zfill(2)} ' \
                       f'{str(match_res[0][0]).zfill(2)}:' \
                       f'{str(match_res[0][1]).zfill(2)}:00'

            elif key is 'this_year':
                return f'{str(datetime.datetime.now().year)}-' \
                       f'{str(ru_months.index(match_res[0][1]) + 1).zfill(2)}-' \
                       f'{str(match_res[0][0]).zfill(2)} ' \
                       f'{str(match_res[0][2]).zfill(2)}:' \
                       f'{str(match_res[0][3]).zfill(2)}:00'

            elif key is 'other_year':
                return f'{str(match_res[0][2])}-' \
                       f'{str(ru_months.index(match_res[0][1]) + 1).zfill(2)}-' \
                       f'{str(match_res[0][0]).zfill(2)} ' \
                       f'{str(match_res[0][3]).zfill(2)}:' \
                       f'{str(match_res[0][4]).zfill(2)}:00'

            break

    return ""
