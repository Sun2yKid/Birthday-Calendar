import os
import datetime

from config import production_config
from lunar import Solar2LunarCalendar

email_file = 'result.html'


def cal_lunar_timedelta(lunar_1, lunar_2):
    """
    lunnar_1 format: "01-01"
    return lunnar_2 - lunnar, days
    """
    # TODO: check
    def weight_lunar_day(lunar_day):
        m, d = lunar_day.split('-')
        print(m, d, lunar_day)
        return int(m) * 30 + int(d)
    lunar_1_weight_value = weight_lunar_day(lunar_1)
    lunar_2_weight_value = weight_lunar_day(lunar_2)
    return lunar_2_weight_value - lunar_1_weight_value


def parse_day(days: list):
    today = datetime.date.today()
    today_lunar_str, today_lunnar = Solar2LunarCalendar(today.strftime('%Y-%m-%d'))
    print('today:', today, 'lunar:', today_lunar_str, today_lunnar)
    for day in days:
        if day['solar']:  # 公历
            remind_day = datetime.datetime.strptime(day['date'], '%Y-%m-%d')
            this_year_remind_day = datetime.date(today.year, remind_day.month, remind_day.day)
            timedelta = this_year_remind_day - today
            day['timedelta'] = timedelta.days
        else:    # 农历
            day['timedelta'] = cal_lunar_timedelta(today_lunar_str, day['date'][-5:])
        if day['offset'] >= day['timedelta'] >= 0:
            day['lunar'] = today_lunnar
            result.append(day)


def write_mail(content: list):
    with open(email_file, 'w', encoding='utf-8') as f:
        f.write('NOTICE:\n')
        for item in content:
            if item['timedelta']:
                text = '%s(%s) is coming in %d days!\n' % (item['title'],
                                                           item['date'] if item['solar'] else '农历' + item['date'],
                                                           item['timedelta'])
            else:
                text = 'Today is %s(%s)!\n' % (item['title'],
                                               item['date'] if item['solar'] else item['lunar'])
            f.write(text)


if __name__ == '__main__':
    result = []
    parse_day(production_config.days)
    print('result', result)
    if result:
        write_mail(result)
    else:
        # if no notification, remove email_file
        if os.path.exists(email_file):
            os.remove(email_file)
