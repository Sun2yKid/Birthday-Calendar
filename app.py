import os
import datetime

from config import production_config
from lunar import Solar2LunarCalendar

email_file = 'result.html'


def parse_day(days: list):
    today = datetime.date.today()
    print('today:', today)
    for day in days:
        if day['solar']:
            remind_day = datetime.datetime.strptime(day['date'], '%Y-%m-%d')
            this_year_remind_day = datetime.date(today.year, remind_day.month, remind_day.day)
            timedelta = this_year_remind_day - today
            day['timedelta'] = timedelta.days
            if day['offset'] >= timedelta.days >= 0:
                result.append(day)
        else:
            today_lunar_str, today_lunnar = Solar2LunarCalendar(today.strftime('%Y-%m-%d'))
            print('lunar:', today_lunar_str, day['date'][-5:])
            if today_lunar_str == day['date'][-5:]:
                day['lunar'] = today_lunnar
                result.append(day)


def write_mail(content: list):
    with open(email_file, 'w', encoding='utf-8') as f:
        f.write('NOTICE:\n')
        for item in content:
            if not item['solar']:
                print(item['lunar'])
                text = 'Today is %s(%s 农历: %r)!\n' % (item['title'], item['date'], item['lunar'])
            elif item['timedelta']:
                text = '%s(%s) is coming in %d days!\n' % (item['title'], item['date'], item['timedelta'])
            else:
                text = 'Today is %s(%s)!\n' % (item['title'], item['date'])
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
